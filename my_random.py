from random import randint
def randch(prob):
    # нужна для обработки вероятности смерти
    N = randint(0, 100)
    if N <= prob:
        return True
    else:
        return False