import pytest
import engine
import torch

@pytest.fixture(scope='module')
def gpt2():
    return engine.Model('gpt2')

@pytest.fixture
def MSG_prompt():
    return "Madison Square Garden is located in the city of"

def test_generation(gpt2:engine.Model, device:str, MSG_prompt:str):

    with gpt2.generate(device_map=device, max_new_tokens=3) as generator:
        with generator.invoke(MSG_prompt) as invoker:
            pass

    output = gpt2.tokenizer.decode(generator.output[0])

    assert output == "Madison Square Garden is located in the city of New York City"

def test_save(gpt2:engine.Model, device:str):

    with gpt2.generate(device_map=device, max_new_tokens=1) as generator:
        with generator.invoke('Hello world') as invoker:

            hs = gpt2.transformer.h[-1].output[0].save()

    assert hs.node.done()
    assert isinstance(hs.value, torch.Tensor)
    assert hs.value.ndim == 3


def test_set(gpt2:engine.Model, device:str):

    with gpt2.generate(device_map=device, max_new_tokens=1) as generator:
        with generator.invoke('Hello world') as invoker:
            
            pre = gpt2.transformer.h[-1].output[0].save()

            gpt2.transformer.h[-1].output[0] = 0

            post = gpt2.transformer.h[-1].output[0].save()

    output = gpt2.tokenizer.decode(generator.output[0])

    assert not (pre.value == 0).all().item()
    assert (post.value == 0).all().item()
    assert output != "Madison Square Garden is located in the city of New"

def test_adhoc_module(gpt2:engine.Model, device:str):

    with gpt2.generate(device_map=device) as generator:
        with generator.invoke('The Eiffel Tower is in the city of') as invoker:
            
            hidden_states = gpt2.transformer.h[-1].output[0]
            hidden_states = gpt2.lm_head(gpt2.transformer.ln_f(hidden_states))
            tokens = torch.softmax(hidden_states, dim=2).argmax(dim=2).save()
        

    output = gpt2.tokenizer.decode(tokens.value[0])

    assert output == "\n-el Tower is a the middle centre Paris"

def test_embeddings_set1(gpt2:engine.Model, device:str, MSG_prompt:str):

    with gpt2.generate(device_map=device, max_new_tokens=3) as generator:
    
        with generator.invoke(MSG_prompt) as invoker:

            embeddings = gpt2.transformer.wte.output

        with generator.invoke("_ _ _ _ _ _ _ _ _") as invoker:

            gpt2.transformer.wte.output = embeddings

    output1 = gpt2.tokenizer.decode(generator.output[0])
    output2 = gpt2.tokenizer.decode(generator.output[1])

    assert output1 == "Madison Square Garden is located in the city of New York City"
    assert output2 == "_ _ _ _ _ _ _ _ _ New York City"

def test_embeddings_set2(gpt2:engine.Model, device:str, MSG_prompt:str):

    with gpt2.generate(device_map=device, max_new_tokens=3) as generator:
    
        with generator.invoke(MSG_prompt) as invoker:

            embeddings = gpt2.transformer.wte.output.save()

    output1 = gpt2.tokenizer.decode(generator.output[0])

    with gpt2.generate(device_map=device, max_new_tokens=3) as generator:

        with generator.invoke("_ _ _ _ _ _ _ _ _") as invoker:

            gpt2.transformer.wte.output = embeddings.value

    output2 = gpt2.tokenizer.decode(generator.output[0])

    assert output1 == "Madison Square Garden is located in the city of New York City"
    assert output2 == "_ _ _ _ _ _ _ _ _ New York City"