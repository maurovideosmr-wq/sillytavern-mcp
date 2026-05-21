import json


def build_v2_card(
    name: str,
    description: str = "",
    personality: str = "",
    scenario: str = "",
    first_mes: str = "",
    mes_example: str = "",
    creator_notes: str = "",
    system_prompt: str = "",
    post_history_instructions: str = "",
    tags: list[str] | None = None,
    alternate_greetings: list[str] | None = None,
    talkativeness: float = 0.5,
    creator: str = "",
    character_version: str = "1.0",
    world: str = "",
    depth_prompt_prompt: str = "",
    depth_prompt_depth: int = 4,
    depth_prompt_role: str = "system",
) -> str:
    tags = tags or []
    alternate_greetings = alternate_greetings or []

    data = {
        "name": name,
        "description": description,
        "personality": personality,
        "scenario": scenario,
        "first_mes": first_mes,
        "mes_example": mes_example,
        "creator_notes": creator_notes,
        "system_prompt": system_prompt,
        "post_history_instructions": post_history_instructions,
        "tags": tags,
        "creator": creator,
        "character_version": character_version,
        "alternate_greetings": alternate_greetings,
        "extensions": {
            "talkativeness": talkativeness,
            "fav": False,
            "world": world,
            "depth_prompt": {
                "prompt": depth_prompt_prompt,
                "depth": depth_prompt_depth,
                "role": depth_prompt_role,
            },
        },
        "character_book": {},
    }

    card = {
        "name": name,
        "description": description,
        "personality": personality,
        "scenario": scenario,
        "first_mes": first_mes,
        "mes_example": mes_example,
        "creatorcomment": creator_notes,
        "avatar": "none",
        "talkativeness": talkativeness,
        "fav": False,
        "tags": tags,
        "spec": "chara_card_v2",
        "spec_version": "2.0",
        "data": data,
    }

    return json.dumps(card, ensure_ascii=False)
