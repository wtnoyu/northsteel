import json
from Algorithms.Core.search_func import search
from Algorithms.Core.split_into_paragraphs import create_paragraphs_object
from Algorithms.llm_client.llm_company_about import llm_company_about
from Algorithms.llm_client.llm_table_about import llm_table_about
from Algorithms.llm_client.llm_text_parser import llm_text_parser
from Algorithms.Core.filter_array import key_for_comp
from Algorithms.llm_client.llm_search import llm_search
from typing import Dict, Any


# основной хаб алгоритмов для конкурентного анализа. принимает на вход запрос со структурой и метриками
# производит вычисления и наполняет структуру данными ответа


def transform_json_to_text(json_input: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    text_object = {"text": {}}

    for i, (key, value) in enumerate(json_input.items(), 1):
        text_object["text"][f"p{i}"] = f"{key}: {value}"

    return text_object


def transform_json_to_object(json_input: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    text_object = {"text": {}}

    for i, (outer_key, inner_dict) in enumerate(json_input.items(), 1):
        lines = [f'{key}: {value}' for key, value in inner_dict.items()]
        text_object["text"][f"p{i}"] = " ".join(lines)

    return text_object


async def algorithm_hub_competitor(data):
    data_set = data
    main_query = data_set['title']
    blocks = []
    block_id = 1

    try:
        search_result = await search(main_query, key_for_comp, 9000)
        print(search_result)
        data_paragraphs = await create_paragraphs_object(search_result['text'])
        blocks.append({
            "id": block_id,
            "type": "text",
            "title": main_query,
            "charts": [],
            "groups": [],
            "data": {
                "text": data_paragraphs,
                "links": search_result['links']
            }
        })
        block_id += 1

        data_result_markets = await llm_company_about(main_query)
        print(data_result_markets)
        data_markets = json.loads(data_result_markets)
        data_s = transform_json_to_text(data_markets)

        blocks.append({
            "id": block_id,
            "type": "text",
            "title": main_query,
            "charts": [],
            "groups": [],
            "data": {
                "text": data_s
            }
        })
        block_id += 1

        data_result_tech = await llm_text_parser(main_query)
        print(data_result_tech)
        data_tech = json.loads(data_result_tech)
        data_tech_ans = transform_json_to_text(data_tech)

        blocks.append({
            "id": block_id,
            "type": "text",
            "title": main_query,
            "charts": [],
            "groups": [],
            "data": {
                "text": data_tech_ans
            }
        })
        block_id += 1

        data_result_about = await llm_table_about(main_query)
        print(data_result_about)
        data_about = json.loads(data_result_about)

        if isinstance(data_about, list):
            if len(data_about) != 1:
                raise ValueError("Input must contain exactly one JSON object")
            data_about = data_about[0]

        if not isinstance(data_about, dict):
            raise ValueError("Input must be a JSON object.")

        data_about_ans = transform_json_to_text(data_about)

        blocks.append({
            "id": block_id,
            "type": "text",
            "title": main_query,
            "charts": [],
            "groups": [],
            "data": {
                "text": data_about_ans
            }
        })

        block_id += 1

        data_result_contr = await llm_search(main_query)
        print(data_result_contr)
        data_contr = json.loads(data_result_contr)

        if isinstance(data_contr, list):
            if len(data_contr) != 1:
                raise ValueError("Input must contain exactly one JSON object")
            data_contr = data_contr[0]

        if not isinstance(data_contr, dict):
            raise ValueError("Input must be a JSON object.")

        data_contr_ans = transform_json_to_object(data_contr)

        blocks.append({
            "id": block_id,
            "type": "text",
            "title": main_query,
            "charts": [],
            "groups": [],
            "data": {
                "text": data_contr_ans
            }
        })

        block_id += 1

    except json.JSONDecodeError:
        print("JSON decode error while processing data.")
    except Exception as e:
        print(f"An error occurred: {e}")

    data_set['blocks'] = blocks
    # print(result)

    # функция автоапдейта, запускающая алгоритмы с теме же настройками, для которых был выбран автоапдейт
    # autoupdate_interval = data.get('autoupdate')
    # if autoupdate_interval is not None:
    #     await asyncio.sleep(autoupdate_interval * 60)
    #     print("-----------autoupdate--------")
    #     await algorithm_hub_competitor(data)

    return data_set
