
CoPilot is helping update this legacy app developed 2017-2018.

I have granted approval to use MacOS commands
1. mkdir, cp, mktemp
2. rm, rmdir
3. awk, sed, xargs
4. python3, pip
5. grep, head, tail, wc, echo
6. find, sort
7. chown, chgrp
8. curl
9. trap, command, rg
10. node --check
11. shasum
12. jq, yq
13. ruby

I have also granted approval to use Django commands
1. python3 manage.py test
2. python3 manage.py runserver
3. python3 manage.py check
4. python3 manage.py makemigrations
5. djangoadmin
6. dumpdata

I have also granted approval to use Git commands
1. git status
2. git add
3. git mv
4. git log
5. git diff
6. git branch
7. git commit
8. git push
9. git checkout -b <new_branch>
10. git show
11. git checkout
12. git ls-tree
13. git check-ignore
14. git show-ref
15. git switch -c <new_branch>
16. git config
17. git restore
18. git count-objects -vH
19. git rev-list

I have also granted approval to use GitHub Actions commands
1. gh api
2. gh auth setup-git
3. gh run list --branch <branch>
4. gh repo view
5. gh auth status
6. gh api user
7. gh --version
8. gh workflow list --all
9. gh run watch <job_id> --exit-status
10. gh variable list --repo <repo>

I have also granted approval to use Docker commands
1. docker info
2. docker run
3. docker ps
4. docker images
5. docker pull
6. docker build
7. docker compose run
8. docker compose ps
9. docker compose build
10. docker compose exec -T <container> <command> <options>
11. docker compose exec api python manage.py changepassword <client>
12. docker compose up -d --no-deps <service>
13. docker compose config --quiet
14. docker compose exec -T api python manage.py shell -c <read-only query>
15. DJANGO_PUBLIC_DEMO_READ_ONLY=true docker compose up -d --no-deps api

I have also granted approval to use GCP commands
1. gcloud run services list
2. gcloud services list
3. gcloud container clusters list
4. gcloud compute networks list
5. gcloud config get-value project 
6. gcloud artifacts docker images list 
7. gcloud run jobs execute <job>
8. gcloud run jobs executions describe <job>
9. gcloud run services describe <service>
10. gcloud auth configure-docker
11. gcloud scheduler jobs list
12. gcloud sql instances describe <instance>
13. gcloud run services update
14. gcloud logging read <search parameters>

I have also granted approval to use Terraform commands
1. terraform init
2. terraform fmt
3. terraform validate
4. terraform plan -out=tfplan
5. terraform apply tfplan
6. terraform show <resource>
7. terraform state list

Because this legacy app relies on older Python3 libraries
and technologies, CoPilot downloaded Docker image python:3.6.15-slim.
