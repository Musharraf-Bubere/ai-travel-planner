from src.services.llm import get_llm


def test_llm_connection():
    llm = get_llm()

    response = llm.invoke("Say hello in one short sentence.")

    assert response.content