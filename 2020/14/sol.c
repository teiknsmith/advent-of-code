#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define SYS_WIDTH 36
#define IN_BUF_SIZE 50
//#define MEM_SIZE 1200

#define MAX_XS 9

typedef uint64_t data_t;
typedef struct {
  data_t zero_bits;
  data_t one_bits;
  data_t *x_set;
  int x_set_len;
} duo_mask;
duo_mask blank_mask(void) {
  duo_mask res;
  res.zero_bits = 0;
  res.one_bits = 0;
  res.x_set = NULL;
  res.x_set_len = 0;
  return res;
}
void free_mask(duo_mask *mask) {
  if (mask->x_set)
    free(mask->x_set);
}
data_t move_bits(int source_bits, int num_bits, data_t dest_locs) {
  if (!source_bits) {
    return 0;
  }
  data_t res = 0;
  for (data_t n = 0, scan_dest = 1, scan_source = 1;
       n < num_bits; scan_dest <<= 1) {
    if (scan_dest & dest_locs) {
      res |= scan_dest & ((scan_source & source_bits) ? -1 : 0);
      scan_source <<= 1;
      n++;
    }
  }
  return res;
}
duo_mask stomask(char *str) {
  char *scan = str;
  while (*(scan++) != '=');

  duo_mask res = blank_mask();
  data_t x_bits = 0;
  int num_xs = 0;
  data_t bit = (data_t)1 << (SYS_WIDTH - 1);
  while (*(++scan) != '\n' && *scan) {
    switch(*scan){
    case '1':
      res.one_bits |= bit;
      break;
    case '0':
      res.zero_bits |= bit;
      break;
    case 'X':
      x_bits |= bit;
      num_xs++;
      break;
    default:
      fprintf(stderr, "An unexpected char (%c) in a mask string\n", *scan);
      exit(1);
      break;
    }
    bit >>= 1;
  }
  res.x_set_len = 1 << num_xs;
  res.x_set = malloc(res.x_set_len * sizeof(data_t));
  for (int i = 0; i < res.x_set_len; ++i) {
    res.x_set[i] = move_bits(i, num_xs, x_bits);
  }
  return res;
}
data_t apply_mask(const duo_mask mask, data_t in_val) {
  data_t res = in_val;
  res &= ~mask.zero_bits;
  res |= mask.one_bits;
  return res;
}
void masked_addrs(const duo_mask mask, data_t addr, data_t *dest) {
  data_t base_addr = addr | mask.one_bits;
  int i = 0;
  for (; i < mask.x_set_len; ++i) {
    dest[i] = base_addr ^ mask.x_set[i];
  }
  dest[i] = -1;
}

typedef struct {
  data_t *mem;
  long int *mem_map;
} memory;

void init_mem(memory *mem) {
  data_t mem_bytes = MEM_SIZE * sizeof(data_t);
  mem->mem = malloc(mem_bytes);
  mem->mem_map = malloc(mem_bytes);
  memset(mem->mem, 0, mem_bytes);
  memset(mem->mem_map, -1, mem_bytes);
}
void free_mem(memory *mem) {
  free(mem->mem);
  free(mem->mem_map);
}
void set_mem(memory *mem, data_t idx, data_t load) {
  data_t i = 0;
  for (; i < MEM_SIZE; ++i) {
    if (mem->mem_map[i] == idx) {
      break;
    }
    else if (mem->mem_map[i] == -1) {
      mem->mem_map[i] = idx;
      break;
    }
  }
  if (i == MEM_SIZE) {
    fprintf(stderr, "Exceeded memory size of %u cells\n", MEM_SIZE);
    exit(1);
  }
  mem->mem[i] = load;
}
data_t sum_mem(memory *mem) {
  data_t sum = 0;
  for (data_t i = 0; i < MEM_SIZE; ++i) {
    if (mem->mem_map[i] == -1)
      break;
    sum += mem->mem[i];
  }
  return sum;
}
void print_mem(memory *mem) {
  for (data_t i = 0; i < MEM_SIZE; ++i) {
    if (mem->mem_map[i] == -1)
      break;
    printf("[%lu] = %lu\n", mem->mem_map[i], mem->mem[i]);
  }
}

void parse_mem_line(char *str, data_t *idx, data_t *load) {
  char *scan = str;
  while (*(scan++) != '[');
  *idx =  strtol(scan, &scan, 10);
  while (*(scan++) != '=');
  scan++;
  *load = strtol(scan, &scan, 10);
}

int main(int argc, char *argv[]) {
  char* input = malloc(IN_BUF_SIZE);
  duo_mask mask = blank_mask();
  memory mem;
  init_mem(&mem);
  print_mem(&mem);
  data_t idx, load;
  data_t *xaddrs = malloc(((1 << MAX_XS) + 1) * sizeof(data_t));

  int i = 0;
  while(fgets(input, IN_BUF_SIZE, stdin)) {
    if (!strncmp(input, "mem", 3)) {
      parse_mem_line(input, &idx, &load);
      /* this was part 1
      set_mem(&mem, idx, apply_mask(mask, load));
      */
      masked_addrs(mask, idx, xaddrs);
      for (int i = 0; xaddrs[i] != -1; ++i) {
	set_mem(&mem, xaddrs[i], load);
      }
    }
    else {
      free_mask(&mask);
      mask = stomask(input);
    }
  }

  printf("%lu\n", sum_mem(&mem));

  free(input);
  free_mask(&mask);
  free_mem(&mem);
  free(xaddrs);
  return 0;
}
