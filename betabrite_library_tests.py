import betabrite

def animation_class_tests():
    """
    Tests for the animation class
    """
    animation = Animation.generate_random()
    # 1 Test parameter validation
    # 1.1 Successful validation
    assert Animation._validate_parameter(, , TextMode.MODE_AUTO)
    # Test animation.generate_random(), which in turn tests animation.randomize()
    assert animation.text == "Random animation"
    assert animation.mode in betabrite.ANIMATION_MODE_DICT.values()
    assert animation.color in betabrite.ANIMATION_COLOR_DICT.values()
    assert animation.position in betabrite.ANIMATION_POSITION_DICT.values()
    # Test 

def run_all_tests():
    print("Running animation class tests")
    animation_class_tests()
    print("Finished animation class tests")
