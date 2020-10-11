Add inline policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "arn:aws:iot:us-east-1:114744974534:topic/home/services/trigger"
        }
    ]
}
```

Configure a test event to turn a light on
```
{
    "domain":"light",
    "service": "turn_on",
    "entity_id": "light.office_light"
}
```
and another to turn the light off
```
{
    "domain":"light",
    "service": "turn_off",
    "entity_id": "light.office_light"
}
```

