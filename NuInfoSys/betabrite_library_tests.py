import betabrite


def test_animation_class() -> None:
    """
    Tests for the animation class
    """
    # 1.0 Test parameter validation
    # 1.1 Successful validation
    # Mode
    assert betabrite.Animation._validate_parameter(betabrite.TextMode.ANIMAL, betabrite.ANIMATION_MODE_DICT,
                                                   betabrite.TextMode.AUTO) == betabrite.TextMode.ANIMAL
    # Color
    assert betabrite.Animation._validate_parameter(betabrite.TextColor.AMBER, betabrite.ANIMATION_COLOR_DICT,
                                                   betabrite.TextColor.AUTO) == betabrite.TextColor.AUTO
    # Animal
    assert betabrite.Animation._validate_parameter(betabrite.TextMode.ANIMAL, betabrite.ANIMATION_MODE_DICT,
                                                   betabrite.TextMode.AUTO) == betabrite.TextMode.ANIMAL
    #
    # 2.0 Test animation.generate_random(), which in turn tests animation.randomize()
    animation: betabrite.Animation = betabrite.Animation.generate_random()
    assert animation.text == "Random animation"
    assert animation.mode in betabrite.ANIMATION_MODE_DICT.values()
    assert animation.color in betabrite.ANIMATION_COLOR_DICT.values()
    assert animation.position in betabrite.ANIMATION_POS_DICT.values()


def run_all_tests():
    """
    Runs all betabrite library tests
    """
    print("Running animation class tests")
    test_animation_class()
    print("Finished animation class tests")
