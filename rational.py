from math import gcd

AUTO_REDUCE = True

class rational:
    def __init__(self, value=0, denom=1):
        if type(value) == rational:
            self.num = value.num
            self.denom = value.denom
        elif type(value) == str:
            if ("/" in value):
                self.num = int(value.split("/")[0])
                self.denom = int(value.split("/")[1])
            # elif value.isnumeric():
            else:
                try:
                    self.num = int(value)
                    self.denom = 1
                except ValueError:
                    raise Exception("if rational initiator is given a string it must be fraction of '<int>/<int>' or a single int")
        else:
            self.num = value
            self.denom = denom

    def __abs__(self):
        return rational(abs(self.num), abs(self.denom))

    def __eq__(self, value):
        if value == None:
            return False
        if (self - value).num == 0:
            return True
        else:
            return False
    def __ne__(self, value):
        if value == None:
            return True
        if (self == value):
            return False
        else:
            return True

    def __add__(self, value):
        return self.add(value)

    def __radd__(self, value):
        return (self + value)

    def __sub__(self, value):
        return self.add(-value)

    def __rsub__(self, value):
        return (self - value)

    def __mul__(self, value):
        return self.multiply(value)

    def __rmul__(self, value):
        return (self * value)

    def __truediv__(self, value):
        return self.divide(value)

    def __rtruediv__(self, value):
        return (self.divide(value).inverse())

    def __neg__(self):
        return (rational(-self.num, self.denom))

    def __iadd__(self, value):
        self.set(self + value)
        return self

    def __isub__(self, value):
        self.set(self - value)
        return self

    def __imul__(self, value):
        self.set(self * value)
        return self

    def __idiv__(self, value):
        self.set(self / value)
        return self

    def __str__(self):
        return self.string()

    def __repr__(self):
        return str(self)

    def HCF(self, value1=None, value2=None):
        if value2 != None:
            # Given two numbers to use
            return gcd(value1, value2)
        elif value1 == None:
            # Assume means to use numerator and denominator
            return gcd(self.num, self.denom)
        else:
            raise Warning("hcf function given exactly one value, must be 0 or 2 only.")
            return 1

    def autoRed(self):
        if self.num == 0:
            self.denom = 1
        if self.denom < 0:
            self.denom *= -1
            self.num *= -1
        if AUTO_REDUCE:
            return self.reduce()
        else:
            return self

    def add(self, value):
        temp1 = rational(self)

        if type(value) == rational:
            temp2 = rational(value)
            hcf = self.HCF(self.denom, value.denom)

            # print("%s * %s = " % (temp1.string(), rational(value.denom, value.denom).string()), end = "")
            temp1.num *= value.denom
            temp1.denom *= value.denom
            temp1.num, temp1.denom = int(temp1.num), int(temp1.denom)
            temp2.num *= self.denom
            temp2.denom *= self.denom
            temp2.num, temp2.denom = int(temp2.num), int(temp2.denom)
            numSum = temp1.num + temp2.num
            result = rational(numSum, temp2.denom)
            # if (result):
            #     print("%s + %s = %s --> %s"%(temp1.string(), temp2.string(), result.string(), result.autoRed().string()))

            return result.autoRed()

        elif type(value) == int:
            result = rational(self.num + self.denom * value, self.denom)
            return result.autoRed()

        else:
            raise TypeError("'Add' method must be given int or rational only.")

    def set(self, value, denom=1):
        # if frac is a list, denom is ignored.
        # if frac and denom are rationals or ints, then they are taken as
        # numerator and denominator
        if type(value) == rational:
            self.num = value.num
            self.denom = value.denom
        elif type(value) == int:
            self.num = value
            self.denom = denom
        elif type(value) == list:
            try:
                self.num = value[0]
                self.denom = value[1]
            except IndexError or len(value) != 2:
                raise IndexError("Length of list 'value' too short, must be of length 2.")
        else:
            raise ValueError("Invalid type for 'value' or 'denom', must be int, list or rational.")

    def reduce(self):
        # Should reduce the fraction down to eliminate common factors
        # return [self.num, self.denom]
        hcf = self.HCF()
        # print("HCF: %d" % (hcf))
        temp = rational(self)
        temp.num /= hcf
        temp.denom /= hcf
        # print("%s --> %s" % (self.string(), temp.string()))
        temp.num, temp.denom = int(temp.num), int(temp.denom)
        # if temp.denom < 0:
        #     temp.num *= -1
        #     temp.denom *= -1
        return temp

    def multiply(self, value):
        temp = rational(self)
        # temp.set(self)
        if type(value) == rational:
            temp.num *= value.num
            temp.denom *= value.denom
        elif type(value) == int:
            temp.num *= value
        else:
            raise ValueError("Invalid type %s for 'value', must be int or rational." % (str(type(value))))
        return temp.autoRed()

    def inverse(self):
        if type(self) == int:
            return rational(1, self)
        else:
            return rational(self.denom, self.num)


    def divide(self, value):
        if type(value) == int:
            value = rational(value)
        if type(value) != rational:
            raise ValueError("Invalid type for 'value', must be int or rational.")
        return self.multiply(value.inverse())

    def string(self):
        if self.denom != 1:
            return ("%d/%d"%(self.num, self.denom))
        else:
            return ("%d"%(self.num))
