# Face Recognition Service

### Usage

#### 1.Build docker image

`sh build-docker-image.sh`

> Generate a docker image. The default image name is **face-service:0.0.1**. To modify it, edit the `docker-config/Dockerfile` and `docker-compose.yml` files.

#### 2.Setting

You can modify the `docker-compose.yml` file to set the service port `APP_PORT` and the face encoding file storage path `FACE_PATH`.

#### 3.Run Service

`docker-compose up -d`

### API

#### 1.Face detect

Url:`/detect`

Method:`POST`

Param:

| Parameter | Type | Descrition
| --- | --- | ---
| `image` | `File` | a photo containing human faces

Response:

```json
{
  "code": 200,
  "data": {
    "face_token": [
      "9d550547-8009-46a5-aa4e-f814d6c12d78"
    ]
  }
}
```

>The `face_token` field will return the face tokens identified in the photo


#### 2.Face recognition

Url:`/verify`

Method:`POST`

Param:

| Parameter | Type | Description
| --- | --- | ---
| `token1` | `string` | face token
| `token2` | `string` | face token
| `threshold` | `int` | The default tolerance value is 0.6 and lower numbers make face 

Response:

```json
{
  "code": 200,
  "data": {
    "result": true
  }
}
```