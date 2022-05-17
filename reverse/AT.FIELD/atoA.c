#include<iostream>
int main ()
{
    char s[17]={'y','O','u','r','_','F','l','a','g','_','i','S','_','h','e','r','e'};//flag=YoUR_fLAG_Is_HeRe
    char c[17]={};
    int a=0;
    while(a<17)
    {
        scanf("%c",&c[a]);
        a++;
    }
    int i=0;
    while(i<17)
    {
        if(c[i]>='A'&&c[i]<='Z')
        {
            c[i]+=32;
        }
        else if(c[i]>='a'&&c[i]!='e')
        {
            c[i]-=32;
        }
        i++;
    }
    int p=0;
    for(int j=0;j<17;j++)
    {
        if(c[j]!=s[j])
        p=1;
    }
    if(p)
    printf("Sorry,Wrong answer");
    else
    printf("Nice!Flag is your input");
    return 0;
}