from brigadier import StringReader

def test_can_read():
    reader = StringReader("abc")
    assert reader.can_read() == True
    reader.skip()
    assert reader.can_read() == True
    reader.skip()
    assert reader.can_read() == True
    reader.skip()
    assert reader.can_read() == False

def test_get_remaining_length():
    reader = StringReader("abc")
    assert reader.get_remaining_length() == 3
    reader.set_cursor(1)
    assert reader.get_remaining_length() == 2
    reader.set_cursor(2)
    assert reader.get_remaining_length() == 1
    reader.set_cursor(3)
    assert reader.get_remaining_length() == 0

def test_can_read_length():
    reader = StringReader("abc")
    assert reader.can_read(1) == True
    assert reader.can_read(2) == True
    assert reader.can_read(3) == True
    assert reader.can_read(4) == False
    assert reader.can_read(5) == False

def test_peek():
    reader = StringReader("abc")
    assert reader.peek() == "a"
    assert reader.get_cursor() == 0
    reader.set_cursor(2)
    assert reader.peek() == "c"
    assert reader.get_cursor() == 2

def test_peek_length():
    reader = StringReader("abc")
    assert reader.peek(0) == "a"
    assert reader.peek(2) == "c"
    assert reader.get_cursor() == 0
    reader.set_cursor(1)
    assert reader.peek(1) == "c"
    assert reader.get_cursor() == 1