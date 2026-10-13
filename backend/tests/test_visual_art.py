from xml.etree import ElementTree

from app.academy.media import svg
from app.academy.visual_art import example_art, icon_for


def test_draw_ground_truth_object_not_wrong_label_or_prediction():
    assert icon_for("Tranh chó, nhãn mèo") == "dog"
    assert icon_for("Máy gọi mèo, tranh là chó") == "dog"
    assert icon_for("Các camera ở lớp") == "idea"


def test_plural_and_counting_pictures_represent_the_actual_quantity():
    root = ElementTree.fromstring(svg(example_art("Two cats")))
    assert len(root.findall("{http://www.w3.org/2000/svg}g")) == 2
    root = ElementTree.fromstring(svg(example_art("2 quả và 3 quả là 5")))
    dots = root.findall("{http://www.w3.org/2000/svg}circle")
    assert len(dots) == 5
    assert sum(dot.attrib["fill"] == "#38a99a" for dot in dots) == 2


def test_named_red_objects_are_red_independently_of_picture_variant():
    for text in ["Cặp đỏ", "Bút chì đỏ", "Táo đỏ"]:
        for variant in range(4):
            assert 'fill="#e87969"' in example_art(text, variant)
