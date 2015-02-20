int getchar_unlocked();

void scanint(int &x)
{
 register int c = getchar_unlocked();
 x = 0;
 for(;(c<48 || c>57);c = getchar_unlocked())
  ;
 for(;c>47 && c<58;c = getchar_unlocked()) 
 {
   x = (x<<1) + (x<<3) + c - 48;
 }
}

void scanint2(int &x)
{
 register int c = getchar_unlocked();
 x = 0;
 while (c<'0' || c>'9')
   {
     c = getchar_unlocked();
   }
 while (c>='0' && c <= '9')
   {
     x = 10*x + (c - '0');
   }
}
