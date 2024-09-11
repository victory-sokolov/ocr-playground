# Fast API OCR Playground

Comparing few OCR libraries

1. [Tesseract](https://github.com/sirfz/tesserocr)
2. [EasyOCR](https://github.com/JaidedAI/EasyOCR)
3. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

Image preprocessing is being done using OpenCV

## Start dev

```shell
cd ocr-app/app
make dev
```

## Generate SSL certificate to run server over https

```bash
brew install mkcert

mkdir ocr-app/app/certs && cd ocr-app/app/certs
mkcert localhost 127.0.0.1 ::1
```

## Run inside Docker

Build Dockerfile `docker build -t ocr . --rm`

Run app inside Docker

```bash
docker run -p 8000:8000 -it --rm ocr-app
```

Run with Kubernetes:

1. Start minikube: `minikube start`
2. Configure your shell to use the Docker daemon inside your Minikube virtual machine `minikube docker-env`
3. Run `eval $(minikube -p minikube docker-env)`
4. Pull docker image: `docker pull victorysokolov/ocr`
5. Apply the Kubernetes deployment config: `kubectl apply -f deployment.yml`

## Terraform

```bash
cd infrastructure/terraform
terraform init
terraform apply
helm list -A # Verfiy installation
```

## ArgoCD

- username: admin
- To retrieve a password
  - `kubectl get secrets argocd-initial-admin-secret -o yaml -n argocd`
  - `echo "copied_password_here" | base64 -d`
  - `kubectl port-forward svc/argocd-server -n argocd 8080:80`
