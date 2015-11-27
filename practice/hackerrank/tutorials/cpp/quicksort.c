





#include <time.h>
#include <stdio.h>

void printArray(int* array, int length);
int* generateRandomArrayOfInts(int size);
int isArraySorted(int* array, int count);




int main()
{

  srand(time(NULL));

  
  //  int sortArray[5] = {9,0,6,2,3};
  int arraySize = 10;
  int* sortArray = generateRandomArrayOfInts(arraySize);
  

  
  
  printf("start work\n");

  quicksortIntArray(sortArray, arraySize);


  


  
  printf("end\n");
  


  if (isArraySorted(sortArray, arraySize))
    {
      printf("SUCCEEDED!\n");
    }
  else
    {
      printf("FAILED\n");
    }



  return 0;
}


int isArraySorted(int* array, int count)
{
  if (count <= 1) return 1;
  int prev = array[0];
  int i = 1;

  for (i = 1; i < count; ++i)
    {
      if (array[i] < prev) return 0;
      prev = array[i];
    }
  return 1;
  
}


int* generateRandomArrayOfInts(int size)
{
  int* intArray = (int*) malloc(size*(sizeof(int)));
  
  if (intArray != NULL)
    {
      int i;
      for (i = 0; i < size; ++i)
	{
	  intArray[i] = rand()%100;
	}

    }
  return intArray;
}



int quicksortIntArray(int* array, int count)
{

  if (count <= 1)
    return 0;

  if (count == 2)
    {
      if (array[0] > array[1])
	{
	  swapElements(array,0,1);
	  
	}
      return 0;

      
    }
  
  printf("quicksorting with count:%d\n");
  printArray(array, count);


  int pivotValue = array[count - 1];
  
  printf("pivotValue is:%d\n",pivotValue);
  
  

  

  int* a = array;
  int* b = &array[count-2];



  while (a < b)
    {
      while (*a <= pivotValue && a <= b)
	{
	  a++;
	}
      while (*b > pivotValue && b >= a)
	{
	  b--;
	}
      if (a < b)
	{
	  int tmp = *a;
	  *a = *b;
	  *b = tmp;
	  a++;
	  b--;
	}
     
    }

  printf("a is at: %d\n", *a);
  //bug here should not swap indiscriminately
  int tmp = *a;
  *a = pivotValue;
  array[count-1] = tmp;

  //a is pivot

  printf("beginning: %d\n", a - array);
  printf("end: %d\n", ((&(array[count])) - a) - 1);


  printArray(array, count);
  
  printf("recurseing\n\n");

  quicksortIntArray(array, (a-array));
  quicksortIntArray(a+1, ((&(array[count])) - a) - 1);

  printf("returned\n\n");
  
  printArray(array, count);
  

  return 0;
}






int swapElements(int* array, int index1, int index2)
{
  int tmp = array[index1];
  array[index1] = array[index2];
  array[index2] = tmp;
  return 0;
}

void printArray(int* array, int length)
{
  printf("[");
  int i;
  for (i = 0; i < length; i++)
    {
      if (i != 0)
	{
	  printf(",");
	}
      printf("%d", array[i]);
    }
  printf("]\n");
  
}
