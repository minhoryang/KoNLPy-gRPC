import glob
import json
import pathlib

ROOT = pathlib.Path.cwd() / "konlpy_grpc_gateway" / "_generated"
RESULT = {}
RESULT["swagger"] = "2.0"
RESULT["info"] = {
    "title": "KoNLPy Service",
    "version": "0.1.0",  # FIXME: pull this from pyproject.toml
    "description": """## KoNLPy("코엔엘파이")는 한국어 정보처리를 위한 파이썬 패키지입니다.
이 서비스는 **KoNLPy의 최신버전(v0.5.2)**을 쉽게 사용해볼 수 있도록 제공된 **OpenResource**입니다.

- KoNLPy의 모든 형태소 분석기를 HTTPS Rest API로 제공합니다.

이 페이지에는 KoNLPy가 제공하는 모든 형태소 분석기가 있습니다.
원하는 분석기를 클릭하고, 해당 분석기가 지원하는 동작을 클릭하여 설명을 보실 수 있습니다.
오른쪽의 **Try it out**을 눌러 직접 요청을 날릴 수 있고, 만들고 있는 프로젝트에서도 편하게 API 요청을 하실 수 있습니다.

해결하지 못한 궁금증은 아래의 **API Support**를 눌러 연락해주세요.
""",
    "contact": {
        "name": "API Support",
        "url": "https://github.com/minhoryang/KoNLPy-gRPC/issues",
    },
    "license": {
        "name": "GNU GPLv3+",
        "url": "https://github.com/minhoryang/KoNLPy-gRPC/blob/master/LICENSE",
    }
}
RESULT["externalDocs"] = {
    "description": "KoNLPy가 제공하는 <형태소 분석 및 품사 태깅>에 대하여 (품사 목록 포함)",
    "url": "http://konlpy.org/ko/latest/morph/",
}
RESULT["consumes"] = ["application/json"]
RESULT["produces"] = ["application/json"]
RESULT["paths"] = {}
RESULT["definitions"] = {}
RESULT["tags"] = []
for swagger_file in ROOT.glob("*.swagger.json"):
    operation_id_prefix = swagger_file.name.split(".")[0]
    if operation_id_prefix in ('global', 'index'):
        continue
    swagger_json = json.loads(swagger_file.read_bytes())
    for path, path_node in swagger_json["paths"].items():
        for method in path_node.values():
            method["operationId"] = f"{operation_id_prefix}{method['operationId']}"
        path = path[len("/v0alpha"):]
        RESULT["paths"][path] = path_node
    RESULT["definitions"].update(swagger_json["definitions"])

# XXX: force override values for Readability.
RESULT["definitions"]["v0alphaStringRequest"]["properties"] = {
    "payload": {
        "type": "string",
        "example": "안녕하세요! 여기에 한국어 문장을 입력해주세요. 저희가 컴퓨터를 이해시키겠습니다.",
    },
    # XXX: "options" removed.
}
RESULT["schemes"] = ["https"]
RESULT["host"] = "endpoint.ainize.ai"
RESULT["basePath"] = "/minhoryang/konlpy-grpc/v0alpha"

RESULT["paths"]["/hannanum/analyze"]["post"]["summary"] = "구문 분석을 합니다."
RESULT["paths"]["/hannanum/morphs"]["post"]["summary"] = "문장에서 형태소를 뽑아냅니다."
RESULT["paths"]["/hannanum/nouns"]["post"]["summary"] = "문장에서 명사를 뽑아냅니다."
RESULT["paths"]["/hannanum/pos09"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다. (9)"
RESULT["paths"]["/hannanum/pos22"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다. (22)"

RESULT["paths"]["/kkma/morphs"]["post"]["summary"] = "문장에서 형태소를 뽑아냅니다."
RESULT["paths"]["/kkma/nouns"]["post"]["summary"] = "문장에서 명사를 뽑아냅니다."
RESULT["paths"]["/kkma/pos"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다."
RESULT["paths"]["/kkma/sentences"]["post"]["summary"] = "문단 내 문장을 구분짓습니다."

RESULT["paths"]["/komoran/morphs"]["post"]["summary"] = "문장에서 형태소를 뽑아냅니다."
RESULT["paths"]["/komoran/nouns"]["post"]["summary"] = "문장에서 명사를 뽑아냅니다."
RESULT["paths"]["/komoran/pos"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다."

RESULT["paths"]["/mecab/morphs"]["post"]["summary"] = "문장에서 형태소를 뽑아냅니다."
RESULT["paths"]["/mecab/nouns"]["post"]["summary"] = "문장에서 명사를 뽑아냅니다."
RESULT["paths"]["/mecab/pos"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다."

RESULT["paths"]["/okt/morphs"]["post"]["summary"] = "문장에서 형태소를 뽑아냅니다."
RESULT["paths"]["/okt/normalize"]["post"]["summary"] = "문장을 정규화 합니다. (예시 포함)"
RESULT["paths"]["/okt/normalize"]["post"]["description"] = "한국어를 처리하는 예시입니닼ㅋㅋㅋㅋㅋ -> 한국어를 처리하는 예시입니다 ㅋㅋ"
RESULT["paths"]["/okt/nouns"]["post"]["summary"] = "문장에서 명사를 뽑아냅니다."
RESULT["paths"]["/okt/phrases"]["post"]["summary"] = "문장 내 어구를 뽑아냅니다. (예시 포함)"
RESULT["paths"]["/okt/phrases"]["post"]["description"] = "한국어를 처리하는 예시입니다 ㅋㅋ -> 한국어, 처리, 예시, 처리하는 예시"
RESULT["paths"]["/okt/pos"]["post"]["summary"] = "문장 내 단어들의 품사를 식별하여 태그를 붙입니다."

# XXX: ordering.
RESULT["tags"].append({
    "name": "Mecab",
    "description": "Mecab기반 은전한닢 한국어 형태소 분석기 (mecab-ko)",
})
RESULT["tags"].append({
    "name": "Okt",
    "description": "오픈소스 한국어 처리기 (open-korean-text, official fork of twitter-korean-text)",
})
RESULT["tags"].append({
    "name": "Komoran",
    "description": "코모란 한국어 형태소 분석기 (powered by shineware)",
})
RESULT["tags"].append({
    "name": "Hannanum",
    "description": "한나눔 한국어 형태소 분석기 (powered by KAIST)",
})
RESULT["tags"].append({
    "name": "Kkma",
    "description": "꼬꼬마 한국어 형태소 분석기 (powered by SNU)",
})

(ROOT / "index.swagger.json").write_text(json.dumps(RESULT))