require 'test/unit'

class Person; end

class TestCheckAttribute < Test::Unit::TestCase
  def setup
    add_checked_attribute(Person, :age)
    @bob = Person.new
  end

  def test_accepts_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
  end

  def test_refuses_nil_values
    assert_raise RuntimeError, 'Invalid attribute' do
      @bob.age = nil
    end
  end

  def add_checked_attribute(klass, attribute)
    eval "
      # klass.class_eval do
      class #{klass}
        def #{attribute}
          @#{attribute}
        end
        def #{attribute}=(value)
          if value.nil?
            raise RuntimeError
          end
          @#{attribute} = value
        end
      end
    "
  end
end
