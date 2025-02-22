from flask import Flask, request
from kubernetes import client, config

app = Flask(__name__)

@app.route('/deploy-model', methods=['POST'])
def deploy_model():
    data = request.get_json()
    model_name = data['modelName']
    deploy_new_model_pod(model_name)
    return 'Model deployment initiated', 200

def deploy_new_model_pod(model_name):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {'name': f'{model_name}-pod'},
        'spec': {
            'containers': [{
                'name': model_name,
                'image': f'models/{model_name}:latest',
                'ports': [{'containerPort': 80}]
            }]
        }
    }
    
    v1.create_namespaced_pod(namespace='default', body=pod_manifest)

if __name__ == '__main__':
    app.run(debug=True)
