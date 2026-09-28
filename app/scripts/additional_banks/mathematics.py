from common import add
# Stem, answer and derivation are authored; oracle expressions are separately evaluated by validate.py.
def rows(skill,data):
 for line in data.strip().splitlines():
  stem,key,a,b,c,why,expr,family,diff=line.split('|')
  add('mathematics',skill,stem,key,[a,b,c],why,'Estimate the size of the result, then check the required operation and units.',int(diff),family,oracleExpression=expr)
rows('number_computation','''
What is 407 + 286?|693|683|703|793|Add ones, tens and hundreds, carrying where needed: 407 + 286 = 693.|407+286|whole addition|1
What is 902 − 478?|424|434|524|476|Regroup across the zero: 902 − 478 = 424. Adding 478 back gives 902.|902-478|regrouping subtraction|1
What is 36 × 24?|864|144|824|964|36 × (20 + 4) = 720 + 144 = 864.|36*24|distributive multiplication|1
What is 1,176 ÷ 28?|42|41|48|52|28 × 40 = 1,120; the remaining 56 is two more groups.|1176/28|whole division|2
What is −14 + 23 − 8?|1|9|17|−1|−14 + 23 = 9, and 9 − 8 = 1.|-14+23-8|signed addition|1
What is (−7)(−6) − 15?|27|−57|57|−27|Two negative factors give 42; subtracting 15 gives 27.|(-7)*(-6)-15|signed multiplication|2
What is 3/4 + 5/8, in simplest form?|11/8|8/12|1/8|13/8|Use eighths: 6/8 + 5/8 = 11/8. Do not add denominators.|3/4+5/8|fraction addition|1
What is 7/9 − 1/6, in simplest form?|11/18|6/3|13/18|5/18|The common denominator is 18: 14/18 − 3/18 = 11/18.|7/9-1/6|fraction subtraction|2
What is 5/12 × 18/25, in simplest form?|3/10|23/37|5/6|3/5|Cancel 5 with 25 and 18 with 12; the product reduces to 3/10.|5/12*18/25|fraction multiplication|2
What is 4/7 ÷ 8/21, in simplest form?|3/2|2/3|32/147|1/2|Multiply 4/7 by the reciprocal 21/8; cancel to get 3/2.|(4/7)/(8/21)|fraction division|2
What is 3.75 + 0.608?|4.358|3.813|4.283|9.83|Align decimal points: 3.750 + 0.608 = 4.358.|3.75+0.608|decimal addition|1
What is 8.4 − 2.76?|5.64|6.36|5.74|6.64|Write 8.40 and subtract 2.76 to get 5.64.|8.4-2.76|decimal subtraction|1
What is 0.36 × 0.5?|0.18|1.8|0.018|0.86|Multiplying by one-half halves 0.36, giving 0.18.|0.36*0.5|decimal multiplication|1
What is 6.72 ÷ 0.8?|8.4|0.84|84|5.376|Multiply both dividend and divisor by 10: 67.2 ÷ 8 = 8.4.|6.72/0.8|decimal division|2
What is 5 + 3 × (12 − 8)?|17|32|20|24|Parentheses give 4, multiplication gives 12, then add 5.|5+3*(12-8)|order of operations|1
What is 2 cubed + 4 squared?|24|20|14|36|2 cubed is 8 and 4 squared is 16; their sum is 24.|2**3+4**2|exponents|1
What is the greatest common factor of 42 and 70?|14|7|21|210|42 = 3 × 14 and 70 = 5 × 14; 3 and 5 share no larger factor.|gcd(42,70)|greatest common factor|2
Two lights flash every 12 and 18 seconds. They flash together now. In how many seconds will they next flash together?|36|6|30|216|The least common multiple of 12 and 18 is 36.|lcm(12,18)|least common multiple|2
Round 47,586 to the nearest hundred.|47600|47500|48000|47000|The tens digit is 8, so increase the hundreds digit and replace tens and ones with zeros.|roundto(47586,100)|rounding|1
What digit occupies the thousandths place in 8.4726?|2|4|7|6|After the decimal, 4 is tenths, 7 hundredths, 2 thousandths and 6 ten-thousandths.|digit(8.4726,3)|place value|1
''')
rows('ratios_percent','''
A box has 18 blue tiles and 12 white tiles. What fraction of all the tiles are blue, in simplest form?|3/5|3/2|2/5|1/2|There are 30 tiles; 18/30 reduces to 3/5. The denominator is the total.|18/(18+12)|part whole ratio|1
A recipe uses 3 cups of oats for 8 bars. How many cups are needed for 24 bars?|9|6|12|8|24 is three times 8, so multiply 3 cups by 3.|3*24/8|direct proportion|1
Five identical notebooks cost $17.50. What is the cost in dollars of eight notebooks?|28|24|30|35|Each notebook costs 17.50/5 = 3.50; eight cost 28.|17.5/5*8|unit price|2
What is 35% of 240?|84|72|96|8.4|30% is 72 and 5% is 12; add to obtain 84.|35/100*240|percent of quantity|1
Twenty-seven is what percent of 90?|30|24|33|3|27/90 = 0.3 = 30%. Divide part by whole.|27/90*100|find percentage|2
A $64 backpack is discounted 25%. What is its sale price in dollars?|48|16|39|50|The discount is 16; subtract from 64, or find 75% of 64.|64*(1-25/100)|discount|2
An item costs $45 before 8% sales tax. What is the total in dollars?|48.6|45.8|53|41.4|Tax is 45 × 0.08 = 3.60; add it to 45.|45*(1+8/100)|sales tax|2
A plant grows from 20 cm to 25 cm. What is the percent increase?|25|20|5|125|The increase is 5 cm; 5/20 × 100 = 25%. Use the original height.|(25-20)/20*100|percent change|2
A club has 32 members. Three-eighths volunteer on Saturday. How many members is that?|12|8|20|24|One-eighth of 32 is 4; three-eighths is 12.|32*3/8|fraction of set|1
Red and yellow beads are in the ratio 4:7. There are 44 beads altogether. How many are yellow?|28|16|25|32|There are 11 ratio parts, each worth 4 beads; yellow has 7 parts.|44/(4+7)*7|ratio total|2
A map scale is 1 cm for every 6 km. Two points are 4.5 cm apart on the map. What is their distance in km?|27|24|10.5|30|Multiply 4.5 by 6 to get 27 km.|4.5*6|map scale|1
A cyclist covers 42 km in 3 hours at a constant speed. How far in km will the cyclist travel in 5 hours?|70|63|75|126|The speed is 14 km per hour; multiply by 5.|42/3*5|constant rate|2
A tank is 60% full and contains 42 liters. What is its capacity in liters?|70|25.2|60|84|If 0.6 of capacity is 42, divide 42 by 0.6.|42/(60/100)|find whole|2
A $50 price is reduced 10%, then the reduced price is reduced another 20%. What is the final price in dollars?|36|35|40|34|After the first reduction it is 45; 80% of 45 is 36. Discounts apply to different bases.|50*(1-10/100)*(1-20/100)|successive discounts|3
In a poll, 56 of 80 students prefer an earlier lunch. What percent is this?|70|56|75|80|56/80 = 7/10 = 70%.|56/80*100|survey proportion|1
A mixture uses 2 parts concentrate to 5 parts water. With 15 cups of water, how many cups of concentrate are needed?|6|5|7.5|10|15 cups is three groups of 5; use three groups of 2.|15/5*2|mixture ratio|2
A car uses 4 gallons of fuel to travel 132 miles. At that rate, how many miles can it travel on 7 gallons?|231|224|264|189|The car travels 33 miles per gallon; 33 × 7 = 231.|132/4*7|fuel unit rate|2
Of 150 tickets, 40% were sold in the morning. Half the remaining tickets sold in the afternoon. How many remain?|45|30|60|75|Morning sales leave 90 tickets; half of 90 remain after the afternoon.|150*(1-40/100)/2|successive fractions|3
A jacket's sale price is $54 after a 10% discount. What was the original price in dollars?|60|59.4|64|48.6|54 is 90% of the original; 54/0.9 = 60.|54/(1-10/100)|reverse discount|3
A model car is 1/24 the length of the real car. The real car is 4.8 meters long. How long is the model in centimeters?|20|2|11.52|200|4.8 meters is 480 cm; 480/24 = 20 cm.|4.8*100/24|scale with conversion|3
''')
rows('measurement','''
How many millimeters are in 3.4 centimeters?|34|340|0.34|3400|There are 10 millimeters per centimeter; multiply by 10.|3.4*10|metric length|1
How many meters are in 2.75 kilometers?|2750|275|27.5|27500|Multiply kilometers by 1,000.|2.75*1000|metric distance|1
How many grams are in 1.08 kilograms?|1080|108|10800|10.8|Multiply kilograms by 1,000.|1.08*1000|metric mass|1
A jug contains 2 liters. After 650 milliliters are poured out, how many milliliters remain?|1350|1450|650|2650|Two liters is 2,000 mL; subtract 650.|2*1000-650|metric capacity subtraction|2
A play begins at 6:45 p.m. and lasts 1 hour 50 minutes. At what time does it end? Give minutes after 8:00 p.m.|35|25|45|55|Adding one hour reaches 7:45; adding 50 minutes reaches 8:35.|(6*60+45+60+50)-8*60|elapsed time|2
How many seconds are in 4 minutes 15 seconds?|255|415|240|195|Four minutes is 240 seconds; add 15.|4*60+15|time conversion|1
Using 12 inches = 1 foot, how many inches are in 5 feet 7 inches?|67|57|60|72|Five feet is 60 inches; add 7.|5*12+7|customary length|1
Using 3 feet = 1 yard, how many yards are in 42 feet?|14|126|39|21|Divide feet by 3.|42/3|customary distance|1
Using 16 ounces = 1 pound, how many ounces are in 2.5 pounds?|40|32|24|48|Two pounds is 32 ounces and half a pound is 8 ounces.|2.5*16|customary mass|2
Using 4 cups = 1 quart, how many cups are in 3.5 quarts?|14|12|7|16|3.5 × 4 = 14 cups.|3.5*4|customary capacity|1
A ribbon is 2.4 m long. Six equal pieces are cut with no waste. What is each piece's length in centimeters?|40|4|24|60|2.4 m is 240 cm; divide by 6.|2.4*100/6|conversion division|2
A thermometer reads −6 degrees. The temperature rises 11 degrees and then falls 4 degrees. What is the final reading?|1|9|−1|−21|−6 + 11 − 4 = 1.|-6+11-4|temperature change|2
A 1.5-liter bottle is used to fill cups holding 250 mL each. How many full cups can it fill?|6|5|4|8|1,500 mL divided by 250 mL per cup gives 6 cups.|1.5*1000/250|capacity quotient|2
A train travels 180 kilometers in 2 hours 30 minutes. What is its average speed in km per hour?|72|90|60|75|2 hours 30 minutes is 2.5 hours, so divide 180 by 2.5.|180/(2+30/60)|rate time conversion|3
A square has side length 30 cm. What is its area in square meters?|0.09|0.9|9|90|The side is 0.3 m; its area is 0.3 squared = 0.09 square meters.|(30/100)**2|squared unit conversion|3
''')
rows('geometry','''
A rectangle is 13 cm long and 7 cm wide. What is its perimeter in cm?|40|91|20|26|Perimeter is twice the sum of length and width: 2 × 20 = 40.|2*(13+7)|rectangle perimeter|1
A rectangle measures 9 m by 6 m. What is its area in square meters?|54|30|15|108|Area is length times width, 9 × 6 = 54.|9*6|rectangle area|1
A square has perimeter 44 cm. What is its area in square centimeters?|121|11|88|484|Each side is 44/4 = 11 cm; 11 squared is 121.|(44/4)**2|perimeter to area|2
A triangle has base 14 cm and perpendicular height 9 cm. What is its area in square centimeters?|63|126|46|31.5|Triangle area is half of base times perpendicular height.|14*9/2|triangle area|2
A parallelogram has base 11 cm and perpendicular height 8 cm. What is its area in square centimeters?|88|44|38|19|Use base times perpendicular height, not a slanted side.|11*8|parallelogram area|1
A trapezoid has parallel bases of 6 cm and 12 cm and height 5 cm. What is its area in square centimeters?|45|90|30|60|Average the bases: 9 cm; multiply by height 5.|(6+12)/2*5|trapezoid area|2
A rectangular prism measures 8 cm by 3 cm by 5 cm. What is its volume in cubic centimeters?|120|79|16|240|Volume is length × width × height = 8 × 3 × 5.|8*3*5|prism volume|1
A cube has side length 4 cm. What is its surface area in square centimeters?|96|64|16|48|Each of six faces has area 16; 6 × 16 = 96.|6*4**2|cube surface area|2
Two angles form a straight angle. One is 68 degrees. How many degrees is the other?|112|22|122|292|A straight angle measures 180 degrees; subtract 68.|180-68|supplementary angles|1
Two angles are complementary. One is 37 degrees. How many degrees is the other?|53|143|63|47|Complementary angles sum to 90 degrees; 90 − 37 = 53.|90-37|complementary angles|1
A triangle has angles of 48 and 67 degrees. How many degrees is its third angle?|65|75|115|85|Triangle angles total 180 degrees; subtract 48 and 67.|180-48-67|triangle angle sum|2
An isosceles triangle has a vertex angle of 44 degrees. How many degrees is each equal base angle?|68|136|44|73|The other two total 136 and are equal, so divide by 2.|(180-44)/2|isosceles angles|2
Using pi = 22/7, what is the circumference in cm of a circle with radius 7 cm?|44|22|154|49|Circumference is 2 × pi × radius = 44 cm.|2*(22/7)*7|circle circumference|2
Using pi = 3.14, what is the area in square centimeters of a circle with radius 5 cm?|78.5|31.4|15.7|157|Area is pi times radius squared: 3.14 × 25.|3.14*5**2|circle area|2
A right triangle has perpendicular legs 6 cm and 8 cm. What is its hypotenuse in cm?|10|14|2|100|6 squared plus 8 squared is 100; the positive square root is 10.|sqrt(6**2+8**2)|pythagorean theorem|2
A rectangular garden is 12 m by 9 m. A 2 m by 3 m corner is removed. What area remains in square meters?|102|108|114|96|Subtract the removed rectangular area 6 from the original 108.|12*9-2*3|composite area|2
A floor is 6 m by 4 m. Square tiles have side length 0.5 m and cover it without gaps. How many tiles are needed?|96|48|24|12|Each tile covers 0.25 square meters; 24/0.25 = 96.|6*4/(0.5**2)|area tiling|3
Two similar triangles have corresponding sides 4 cm and 10 cm. A second side of the smaller triangle is 6 cm. What is the matching side of the larger triangle in cm?|15|12|24|8.4|The scale factor is 10/4 = 2.5; multiply 6 by 2.5.|6*10/4|similar figures|3
A point moves from (−3, 2) to (5, 2). What distance does it travel along the horizontal line?|8|2|6|10|The y-coordinate stays fixed; the horizontal distance is 5 − (−3) = 8.|5-(-3)|coordinate distance|2
A rectangular box has volume 180 cubic centimeters, length 9 cm and width 4 cm. What is its height in cm?|5|20|45|13|Divide volume by the base area: 180/(9 × 4) = 5.|180/(9*4)|missing prism dimension|2
''')
rows('algebra','''
Solve x + 17 = 42.|25|59|35|24|Subtract 17 from both sides.|42-17|one step addition equation|1
Solve 6x = 54.|9|48|60|324|Divide both sides by 6.|54/6|one step multiplication equation|1
Solve 3x − 5 = 22.|9|17/3|7|27|Add 5 to obtain 3x = 27, then divide by 3.|(22+5)/3|two step equation|2
Solve 4(x + 2) = 36.|7|11|8|34|Divide by 4 to get x + 2 = 9, then subtract 2.|36/4-2|parenthesized equation|2
Solve 5x + 7 = 2x + 28.|7|21|35/3|5|Subtract 2x and 7 to get 3x = 21, so x = 7.|(28-7)/(5-2)|both sides equation|3
If a = 4 and b = −3, what is 2a − b?|11|5|−2|−11|Substitute: 8 − (−3) = 11.|2*4-(-3)|substitution signed|2
What is the coefficient of x after simplifying 7x − 2x + 3x?|8|12|2|5|Combine the coefficients: 7 − 2 + 3 = 8.|7-2+3|like terms|1
When 3(2x − 5) is expanded, what is its constant term?|−15|−5|15|6|Distribute 3 to both terms, giving 6x − 15.|3*(-5)|distributive property|2
A number increased by twice itself is 39. What is the number?|13|19.5|37|26|Let the number be x; x + 2x = 39 gives 3x = 39.|39/3|translate equation|2
A taxi charges $4 plus $3 per mile. A ride costs $25. How many miles was the ride?|7|21|9|8|Subtract the fixed $4, then divide the remaining $21 by 3.|(25-4)/3|linear cost|2
Three consecutive integers have sum 72. What is the largest?|25|24|23|26|The middle integer is 72/3 = 24; the largest is one more.|72/3+1|consecutive integers|3
Solve x/5 + 3 = 11.|40|8|70|14|Subtract 3 to get x/5 = 8, then multiply by 5.|(11-3)*5|fractional equation|2
If y = 2x squared − 3, what is y when x = −2?|5|−11|13|1|Square −2 first to get 4; 2 × 4 − 3 = 5.|2*(-2)**2-3|quadratic substitution|2
A rectangle's length is 3 cm more than its width. Its perimeter is 30 cm. What is its width in cm?|6|9|12|13.5|2w + 2(w + 3) = 30, so 4w = 24 and w = 6.|(30-2*3)/4|geometry equation|3
What is the greatest integer x satisfying 2x + 1 < 12?|5|6|11|4|Subtract 1 and divide by 2: x < 5.5, so the greatest integer is 5.|greatest_int_lt(2,1,12)|strict inequality|3
''')
rows('statistics_probability','''
What is the mean of 7, 9, 12 and 16?|11|10|12|44|Their sum is 44; divide by four values.|(7+9+12+16)/4|arithmetic mean|1
What is the median of 4, 11, 7, 15 and 8?|8|7|9|11|Order the values 4, 7, 8, 11, 15; the middle is 8.|median(4,11,7,15,8)|odd median|1
What is the median of 3, 6, 8, 13, 14 and 20?|10.5|8|13|11|The middle pair is 8 and 13; average them to get 10.5.|median(3,6,8,13,14,20)|even median|2
What is the range of 18, 25, 14, 30 and 22?|16|14|22|30|Range is maximum minus minimum: 30 − 14.|30-14|range|1
Scores are 6, 8, 8, 9, 10, 10, 10 and 12. What is the mode?|10|8|9|12|10 appears three times, more often than any other score.|mode(6,8,8,9,10,10,10,12)|mode|1
A bag holds 5 red, 3 blue and 2 green counters. One counter is chosen at random. What is the probability it is blue, in simplest form?|3/10|3/7|1/3|7/10|There are 3 blue counters among 10 equally likely counters.|3/(5+3+2)|simple probability|1
A fair six-sided die is rolled. What is the probability of an outcome greater than 4, in simplest form?|1/3|1/2|2/3|1/6|The favorable outcomes are 5 and 6: 2 out of 6, or 1/3.|2/6|event counting|1
Two fair coins are tossed independently. What is the probability both show heads?|1/4|1/2|3/4|1|The four equally likely outcomes are HH, HT, TH and TT; only HH qualifies.|1/2*1/2|independent events|2
Four tests have mean score 82. The first three scores are 76, 85 and 81. What is the fourth score?|86|82|84|90|The required total is 4 × 82 = 328; subtract the known total 242.|4*82-76-85-81|missing mean value|3
A bag has 4 black and 2 white counters. Two are drawn without replacement. What is the probability both are white, in simplest form?|1/15|1/9|1/3|2/15|The first white probability is 2/6; after one white is removed it is 1/5. Multiply to get 1/15.|2/6*1/5|dependent events|3
''')
