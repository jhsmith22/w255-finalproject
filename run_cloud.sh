#!/bin/bash

NAMESPACE=jhsmith

# Run pytest within poetry virtualenv
poetry env remove python3.10
poetry install
poetry run pytest -vv -s

# Set context (DIFFERENT)
echo "Set kubernetes context"
kubectl config use-context w255-aks

echo "Apply Kustomize Files"
kubectl kustomize ./.k8s/overlays/prod/ | kubectl apply -f -
kubectl get all -n $NAMESPACE

echo "Wait for API to be accessible"
# # wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET 'https://jhsmith.mids255.com/health')
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 1
    fi
done

echo "testing '/docs' endpoint. expect status code of 200 returned"
curl -o /dev/null -s -w "%{http_code}\n" -X GET 'https://jhsmith.mids255.com/docs'

echo "testing '/health' endpoint. expect status code of 200 returned"
curl -o /dev/null -s -w "%{http_code}\n" -X GET 'https://jhsmith.mids255.com/health'

# # # echo "testing '/predict' endpoint. expect status code of 200 returned"
curl -X 'POST' 'https://jhsmith.mids255.com/predict' -L -H 'Content-Type: application/json' -d \
'{"text": ["I hate you.", "I love you."]}'

echo "Delete deployments and services in namespace"
kubectl delete --all deployments --namespace=${NAMESPACE}
kubectl delete --all services --namespace=${NAMESPACE}
kubectl delete virtualservice lab4 -n ${NAMESPACE}