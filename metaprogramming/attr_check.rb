class C
  def self.attr_check attr, &check
    define_method attr do
      self.instance_variable_get("@#{attr}")
    end
    define_method "#{attr}=" do |var|
      self.instance_variable_set("@#{attr}", (check.call(var)? var : nil))
    end
  end

  attr_check :var do
    |v| v>= 10
  end

  attr_check :var2 do
    |v| v>= 10
  end
end

c = C.new
c.var = 9
c.var2 = 10
puts c.var
puts c.var2

