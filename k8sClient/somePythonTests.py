

podTemplate = {
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
    "name": "mypod"
  },
  "spec": {
    "containers": [
      {
        "image": "python:3",
        "name": "mypod",
        "volumeMounts": [
          {
            "name": "azure",
            "mountPath": "/mnt/azure"
          }
        ]
      }
    ],
    "volumes": [
      {
        "name": "azure",
        "azureFile": {
          "secretName": "azure-secret",
          "shareName": "aksshare",
          "readOnly": "false"
        }
      }
    ]
  }
}

print(podTemplate)