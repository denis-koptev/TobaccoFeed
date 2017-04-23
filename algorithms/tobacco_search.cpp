#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>

std::string replace_up(std::string src)
{
	char * c_inp = new char[src.size()];
	strcpy(c_inp, src.c_str());
	return strlwr(c_inp);
}

void erase(std::string & src, char symbol)
{
	src.erase(std::remove(src.begin(), src.end(), symbol), src.end());
}

int main() 
{

	const int dim = 1000;

	std::vector<std::string> tobaccos;


	for (int i = 0; i < dim; ++i)
	{
		tobaccos.push_back("tobacco_" + std::to_string(i));
		//std::cout << tobaccos.back() << std::endl;
	}

	tobaccos[999] = "afzal_pan-raas";
	tobaccos[777] = "adalya_mango_tango";

	std::string init_input = "a";

	std::string input = replace_up(init_input);
	erase(input, ' ');
	erase(input, '-');

	std::cout << input << std::endl;

	int max_eq = 0;
	int max_idx = -1;

	for (int i = 0; i < dim; ++i)
	{

		std::string curr = tobaccos[i];

		erase(curr, '_');
		erase(curr, '-');
		replace_up(curr);


		int curr_eq = 0;
		int curr_idx = i;

		for (int j = 0; j < input.size(); ++j)
		{
			int pos;
			while ((pos = curr.find(input[j])) != std::string::npos)
			{
				curr_eq++;
				curr.erase(pos, 1);
			}
			
		}

		if (curr_eq > max_eq)
		{
			max_eq = curr_eq;
			max_idx = curr_idx;
		}
	}

	if (max_idx != -1)
	{
		std::cout << "FOUND: " << init_input << " WITH TOBACCO " << tobaccos[max_idx] << "; SYMBOLS: " << max_eq << std::endl;
	}
	else
	{
		std::cout << "NOT FOUND" << std::endl;
	}

	return 0;

}