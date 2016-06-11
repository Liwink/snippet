def def_methods
  shared = 0
  Kernel.send :define_method, :counter do
    shared
  end
  Kernel.send :define_method, :inc do |x|
    shared += x
  end
end
def_methods

p counter
p inc(4)
p counter
