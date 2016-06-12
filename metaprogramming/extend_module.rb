module M
  class << self
    def m; puts 'm'; end
  end
end

module MM
  def mm; puts 'mm'; end
end

module MMM
  def mmm; puts 'mmm'; end
end

class S
  class << self
    def s; puts 's'; end
  end
end

class C < S
  include M

  class << self
    include MM
  end

end

C.extend MMM

C.s
C.mm
C.mmm
C.m
