#include <iostream>
#include <numeric>
#include <cstdlib>

// Kolaylık olsun
using namespace std;

// Tipik bir C++ fonksiyonu 
void carp(int n, float *x, float *y, float *z)
{
  for (int i = 0; i < n; i++)
  {
      z[i] = x[i] * y[i];
  }   
}


// Ustteki fonksiyonun CUDA versiyonu
__global__
void carp_cuda(int n, float *x, float *y, float *z)
{
  for (int i = threadIdx.x; i < n; i += blockDim.x)
  {
      z[i] = x[i] * y[i];
  }       
}

int main(int argc, char *argv[])
{
  // Çok büyük bir sayı belirleyelim
  int N = 10000;

  float *x_gpu, *y_gpu, *z_gpu, *x_cpu, *y_cpu, *z_cpu;

  // GPU ve CPU tarafindan ulasilabilen memory ayirtalim
  cudaMallocManaged(&x_gpu, N * sizeof(float));
  cudaMallocManaged(&y_gpu, N * sizeof(float));
  cudaMallocManaged(&z_gpu, N * sizeof(float));

  // Sadece CPU tarafindan ulasilabilen memory ayirtalim
  x_cpu = new float[N];
  y_cpu = new float[N];
  z_cpu = new float[N];

  // 
  for (int i = 0; i < N; ++i) {
    x_gpu[i] = 1.0f;
    y_gpu[i] = 2.0f;
    x_cpu[i] = 1.0f;
    y_cpu[i] = 2.0f;
  }

  // Fonksiyonu GPU'da argv[1] blokta ve her blokta argv[2] thread
  // olacak sekilde çagiralım
  int blok_sayisi = atoi(argv[1]);
  int thread_sayisi = atoi(argv[2]);

  carp_cuda<<<blok_sayisi, thread_sayisi>>>(N, x_gpu, y_gpu, z_gpu);

  // GPU'yu bekleyelim de isini bitirsin, yoksa ortam karisir.
  cudaDeviceSynchronize();

  // Normal CPU fonlsiyonunu çagiralım
  carp(N, x_cpu, y_cpu, z_cpu);

  // Bakalim dogru mu yaptik?
  // z_gpu ve z_cpu ayni degerlere sahip olması lazim 
  for(int i = 0; i < N; ++i) 
      cout << z_cpu[i] << " " << z_gpu[i] << endl;

  // Release the Kraken - Kraken'i saliverin gelsin. 
  cudaFree(x_gpu);
  cudaFree(y_gpu);
  cudaFree(z_gpu);
  delete [] x_cpu;
  delete [] y_cpu;
  delete [] z_cpu;
  
  return 0;
}
