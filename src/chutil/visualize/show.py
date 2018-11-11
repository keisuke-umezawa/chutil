import chainer
from chainer.training import extensions
from typing import Any, Iterable
from IPython.display import Image, display


def show_test_performance(
    model: chainer.Chain, test: Iterable[Any], *, device: int = 0, batchsize: int = 256
) -> None:
    if device >= 0:
        model.to_gpu()
    test_iter = chainer.iterators.SerialIterator(
        test, batchsize, repeat=False, shuffle=False
    )
    test_evaluator = extensions.Evaluator(test_iter, model, device=device)
    results = test_evaluator()
    print("Test accuracy:", results["main/accuracy"])


def show_graph(out_dir: str = "./out/") -> None:
    import pydot

    graph = pydot.graph_from_dot_file(out_dir + "cg.dot")  # load from .dot file
    graph[0].write_png("graph.png")
    display(Image("graph.png", width=600, height=600))


def show_loss_and_accuracy(out_dir: str = "./out/") -> None:
    display(Image(filename=out_dir + "loss.png"))
    display(Image(filename=out_dir + "accuracy.png"))
