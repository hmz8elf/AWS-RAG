
EVAL_DATASET = [
    {
        "question": "Quel service AWS utiliser pour du stockage objet ?",
        "ground_truth": "Amazon S3 est le service de stockage objet d'AWS."
    },
    {
        "question": "Comment créer un bucket S3 avec AWS CLI ?",
        "ground_truth": "aws s3 mb s3://nom-du-bucket ou aws s3api create-bucket --bucket nom-du-bucket --region eu-west-1"
    },
    {
        "question": "Quel service AWS pour exécuter du code sans serveur ?",
        "ground_truth": "AWS Lambda permet d'exécuter du code sans gérer de serveurs."
    }
]