import glob
import json
import pathlib

ROOT = pathlib.Path.cwd() / "konlpy_grpc_gateway" / "_generated"
RESULT = {}
RESULT["swagger"] = "2.0"
RESULT["info"] = {}
RESULT["info"]["title"] = "KoNLPy Service"
RESULT["info"]["version"] = "0.1.0"
RESULT["consumes"] = ["application/json"]
RESULT["produces"] = ["application/json"]
RESULT["paths"] = {}
RESULT["definitions"] = {}
for swagger_file in ROOT.glob("*.swagger.json"):
    operation_id_prefix = swagger_file.name.split(".")[0]
    swagger_json = json.loads(swagger_file.read_bytes())
    for path in swagger_json["paths"].values():
        for method in path.values():
            method["operationId"] = f"{operation_id_prefix}{method['operationId']}"
    RESULT["paths"].update(swagger_json["paths"])
    RESULT["definitions"].update(swagger_json["definitions"])

(ROOT / "index.swagger.json").write_text(json.dumps(RESULT))