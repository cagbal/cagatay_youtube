#include <iostream>
#include <numeric>
#include <cstdlib>

// Kolaylýk olsun
using namespace std;

// Tipik bir C++ fonksiyonu 
void carp(int n, float *x, float *y, float *z)
{
  for (int i = 0; i < n; i++)
  {
      z[i] = x[i] * y[i];
  }   
}


// Üstteki fonksiyonun CUDA versiyonu
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
  // Çok büyük bir sayý belirleyelim
  int N = 10000;

  float *x_gpu, *y_gpu, *z_gpu, *x_cpu, *y_cpu, *z_cpu;

  // GPU ve CPU tarafýndan ulaþalýbilen memory ayýrtalým
  cudaMallocManaged(&x_gpu, N * sizeof(float));
  cudaMallocManaged(&y_gpu, N * sizeof(float));
  cudaMallocManaged(&z_gpu, N * sizeof(float));

  // Sadece CPU tarafýndan ulaþýlabilen memory ayýrtalým
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
  // olacak þekilde çaðýralým
  int blok_sayisi = atoi(argv[1]);
  int thread_sayisi = atoi(argv[2]);

  carp_cuda<<<blok_sayisi, thread_sayisi>>>(N, x_gpu, y_gpu, z_gpu);

  // GPU'yu bekleyelim de iþini bitirsin, yoksa ortam karýþýr.
  cudaDeviceSynchronize();

  // Normal CPU fonsiyonunu çaðýralým
  carp(N, x_cpu, y_cpu, z_cpu);

  // Bakalým doðru mu yaptýk?
  // z_gpu ve z_cpu ayný deðerlere sahip olmasý lazým 
  for(int i = 0; i < N; ++i) 
      cout << z_cpu[i] << " " << z_gpu[i] << endl;

  // Release the Kraken - Kraken'ý salýverin gelsin. 
  cudaFree(x_gpu);
  cudaFree(y_gpu);
  cudaFree(z_gpu);
  delete [] x_cpu;
  delete [] y_cpu;
  delete [] z_cpu;
  
  return 0;
}

