syms s1 c1 s2 c2 s3 c3 L1 L2 L3
T1 = [c1 -s1 0 L1*c1; s1 c1 0 L1*s1; 0 0 1 0; 0 0 0 1]

T2 = [c2 -s2 0 L2*c2; s2 c2 0 L2*s2; 0 0 1 0; 0 0 0 1]

T3 = [c3 -s3 0 L3*c3; s3 c3 0 L3*s3; 0 0 1 0; 0 0 0 1]

HTM = T1*T2*T3


HTM = subs(HTM, [L1 L2 L3], [103, 103, 22])

position = HTM(:,4)

angle1 = pi/4
angle2 = pi/4
angle3 = pi/4
ss1 = sin(angle1)
cc1 = cos(angle1)

ss2 = sin(angle2)
cc2 = cos(angle2)

ss3 = sin(angle3)
cc3 = cos(angle3)

position = subs(position, [s1 c1 s2 c2 s3 c3], [ss1 cc1 ss2 cc2 ss3 cc3])
position(1)
position(2)
double(position(1))
double(position(2))