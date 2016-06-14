require 'test/unit'
require 'pry'

module CheckedAttributes
  def self.included(klass)
    klass.extend ClassMethods
  end

  module ClassMethods
    def attr_checked(attribute, &validation)
      define_method attribute do
        instance_variable_get("@#{attribute}")
      end

      define_method "#{attribute}=" do |value|
        raise "Invalid attribute" unless validation.call(value)
        instance_variable_set("@#{attribute}", value)
      end
    end
  end
end

class Person
  include CheckedAttributes
  attr_checked :age do |v|
    v >= 18
  end
end

class TestCheckedAttributes < Test::Unit::TestCase
  def setup
    @bob = Person.new
  end

  def test_accepts_valid_values
    @bob.age = 20
    assert_equal 20, @bob.age
  end

  def test_refuse_invalid_values
    assert_raise RuntimeError, 'Invalid attribute' do
      @bob.age = 17
    end
  end

end

