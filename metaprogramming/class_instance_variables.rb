class MyClass
  @my_var = 1
  def self.read; p @my_var; end
  def write; @my_var = 2; end
  def read; p @my_var; end
end

obj = MyClass.new
obj.read
obj.write
obj.read
MyClass.read
