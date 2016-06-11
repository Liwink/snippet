class C
  def out
    puts 'out'
    def inner
      puts 'inner'
    end
  end
end

c = C.new
c.out
c.inner
