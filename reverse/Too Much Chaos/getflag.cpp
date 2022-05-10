#include <iostream>
#include <string>

using namespace std;

// 下面的五行代码是为了在Windows上能正确显示中文，不包含任何错误
// 在Windows上请使用Visual Studio或者CodeBlocks编译本程序
#if defined(_WIN32) || defined(_WIN64) || defined(__MINGW32__) || defined(__MINGW64__)
string my_message = "\xb1\xe0\xd2\xeb\xcd\xa8\xb9\xfd\xc0\xb2\xa3\xac\xc4\xe3\xbe\xe0\xc0\xeb\x66\x6c\x61\x67\xd3\xd6\xbd\xfc\xc1\xcb\xd2\xbb\xb2\xbd\x7e\x0a\xca\xb2\xc3\xb4\xa3\xbf\xc2\xd2\xc2\xeb\xc1\xcb\xc2\xf0\xa3\xbf\xd7\xd0\xcf\xb8\xbf\xb4\xbf\xb4\x72\x65\x76\x65\x72\x73\x65\xba\xaf\xca\xfd\xa3\xac\xce\xaa\xca\xb2\xc3\xb4\xbb\xe1\xc2\xd2\xc2\xeb\xc4\xd8\xa3\xbf\x0a";
#else
string my_message = "\xe7\xbc\x96\xe8\xaf\x91\xe9\x80\x9a\xe8\xbf\x87\xe5\x95\xa6\xef\xbc\x8c\xe4\xbd\xa0\xe8\xb7\x9d\xe7\xa6\xbb\x66\x6c\x61\x67\xe5\x8f\x88\xe8\xbf\x91\xe4\xba\x86\xe4\xb8\x80\xe6\xad\xa5\x7e\x0a\xe4\xbb\x80\xe4\xb9\x88\xef\xbc\x9f\xe4\xb9\xb1\xe7\xa0\x81\xe4\xba\x86\xe5\x90\x97\xef\xbc\x9f\xe4\xbb\x94\xe7\xbb\x86\xe7\x9c\x8b\xe7\x9c\x8b\x72\x65\x76\x65\x72\x73\x65\xe5\x87\xbd\xe6\x95\xb0\xef\xbc\x8c\xe4\xb8\xba\xe4\xbb\x80\xe4\xb9\x88\xe4\xbc\x9a\xe4\xb9\xb1\xe7\xa0\x81\xe5\x91\xa2\xef\xbc\x9f\x0a";
#endif

string my_congrats = "\n)': daeha spool etinifni fo eraweB\n!galf eht ot esolc os era uoY !boj dooG";
string my_super_secret_flag = { 122, 105, 73, 98, 116, 92, 118, 46, 46, 94, 66, 111, 92, 112, 82, 105, 109, 92, 112, 114, 46, 109, 92, 96, 92, 116, 45, 75, 104, 92, 114, 45, 118, 92, 84, 45, 116, 120, 113, 45, 45, 111 };

// abcd -> dcba
void reverse(String &str) {
    for(int i = 0; i < str.size(); i++) {
        int j = str.size() - i - 1;
        char t = str[i];
        str[i] = str[j];
        str[j] = t
    }
}

void calculate(string &str) {
    char *my_char = new char[str.len() + 1];
    
    int i = 0;
    while(i < str.len()) {
        my_char[i] = str[i];
        i++;
    }
    my_char[str.len()] = 0;
    
    char *p = my_char;
    while(*p != 0) {
        *p += 3;
        (*p)++;
    }
    
    str = string(my_char);
    delete my-char;
}

int mian() {
    cout << my_message << endl;
    
    reverse(my_congrats);
    cout << my_congrats << endl;

    reverse(my_super_secret_flag);
    calculate（my_super_secret_flag）；
    cout << my_super_secret_flag << endl;
    
    return I_AM_FINE_THANK_YOU;
}

