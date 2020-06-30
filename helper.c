#define PY_SSIZE_T_CLEAN
#include <python3.8/Python.h>
#include <python3.8/structmember.h>

//mfederczuk zone
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

enum { GET_RENDER_BUCK_VECTOR_INIT_CAPACITY = 1024 };

#define GET_RENDER_BUCK_VECTOR_CAPACITY_GROW_FACTOR 1.5

/**
 * Pair of `uint_fast64_t`.
 */
struct uint_pair {
	uint_fast64_t first;
	uint_fast64_t second;
};

/**
 * A pair of a `uint_fast64_t` vector and a `uint_pair` vector.
 *
 * `*_begin` is the location of the first element of the vector.
 * `*_end` is the location one after the last element of the vector.
 * If the vector is empty `*_begin` and `*_end` point towards the same location.
 */
struct uint_vector__uint_pair_vector__pair {
	uint_fast64_t* first_begin;
	uint_fast64_t* first_end;

	struct uint_pair* second_begin;
	struct uint_pair* second_end;
};

/**
 * `items_begin` must be the pointer to the location of the first item.
 * `items_end` must be the pointer to the location one after the last item.
 * If it should be empty, `items_begin` and `items_end` should be pointers to
 * the same location.
 *
 * The members `uint_vector__uint_pair_vector__pair::first_begin` and
 * `uint_vector__uint_pair_vector__pair::second_begin` of the return value must
 * be manually freed.
 *
 * If an error occurs, `uint_vector__uint_pair_vector__pair::first_begin` will
 * be set to `NULL` and `errno` will be set accordingly.
 * Accessing the other members in this case is undefined behaviour.
 */
struct uint_vector__uint_pair_vector__pair get_render_buck(uint_fast64_t* items_begin, uint_fast64_t* items_end) {
	#define _return_err \
		return ((struct uint_vector__uint_pair_vector__pair){ \
			.first_begin = NULL \
		})


	uint_fast64_t* iteml_begin = malloc(sizeof(uint_fast64_t) * GET_RENDER_BUCK_VECTOR_INIT_CAPACITY);
	if(iteml_begin == NULL) _return_err;
	
	uint_fast64_t* iteml_end     = iteml_begin;
	uint_fast64_t* iteml_cap_end = iteml_begin + GET_RENDER_BUCK_VECTOR_INIT_CAPACITY;


	struct uint_pair* itemq_begin = malloc(sizeof(struct uint_pair) * GET_RENDER_BUCK_VECTOR_INIT_CAPACITY);
	if(itemq_begin == NULL) {
		int tmp = errno;
		free(iteml_begin);
		errno = tmp;
		_return_err;
	}

	struct uint_pair* itemq_end     = itemq_begin;
	struct uint_pair* itemq_cap_end = itemq_begin + GET_RENDER_BUCK_VECTOR_INIT_CAPACITY;


	uint_fast64_t sindex = 0;
	uint_fast64_t bindex = 0;


	const size_t items_size = (items_end - items_begin);
	for(size_t i = 0; i < items_size; ) {
		const uint_fast64_t sit = items_begin[i];
		++i;

		uint_fast64_t bit = sit + 1;
		bindex = sindex + 1;

		while(i < items_size && bit == items_begin[i]) {
			++bit;
			++bindex;
			++i;
		}

		if(sit + 1 == bit) {
			if(iteml_end == iteml_cap_end) {
				const size_t old_cap = (iteml_cap_end - iteml_begin);
				const size_t new_cap = old_cap * GET_RENDER_BUCK_VECTOR_CAPACITY_GROW_FACTOR;

				uint_fast64_t* const tmp = realloc(iteml_begin, sizeof(uint_fast64_t) * new_cap);
				if(tmp == NULL) {
					int tmp = errno;
					free(iteml_begin);
					free(itemq_begin);
					errno = tmp;
					_return_err;
				}

				iteml_begin = tmp;
				iteml_end = iteml_begin + old_cap;
				iteml_cap_end = iteml_begin + new_cap;
			}

			(*iteml_end) = sindex;
			++iteml_end;
		} else {
			if(itemq_end == itemq_cap_end) {
				const size_t old_cap = (itemq_cap_end - itemq_begin);
				const size_t new_cap = old_cap * GET_RENDER_BUCK_VECTOR_CAPACITY_GROW_FACTOR;

				struct uint_pair* const tmp = realloc(itemq_begin, sizeof(struct uint_pair) * new_cap);
				if(tmp == NULL) {
					int tmp = errno;
					free(iteml_begin);
					free(itemq_begin);
					errno = tmp;
					_return_err;
				}

				itemq_begin = tmp;
				itemq_end = itemq_begin + old_cap;
				itemq_cap_end = itemq_begin + new_cap;
			}

			(*itemq_end) = (struct uint_pair){
				.first = sindex,
				.second = bindex
			};
			++itemq_end;
		}

		sindex = bindex;
	}

	// shrinking the vector capacity to the size; removing unused storage

	if(iteml_end != iteml_cap_end) {
		const size_t old_cap = (iteml_cap_end - iteml_begin);
		const size_t new_cap = (iteml_end - iteml_begin);

		uint_fast64_t* const tmp = realloc(iteml_begin, sizeof(uint_fast64_t) * new_cap);
		if(tmp == NULL) {
			int tmp = errno;
			free(iteml_begin);
			free(itemq_begin);
			errno = tmp;
			_return_err;
		}

		iteml_begin = tmp;
		iteml_end = iteml_begin + new_cap;
	}

	if(itemq_end != itemq_cap_end) {
		const size_t old_cap = (itemq_cap_end - itemq_begin);
		const size_t new_cap = (itemq_end - itemq_begin);

		struct uint_pair* const tmp = realloc(itemq_begin, sizeof(struct uint_pair) * new_cap);
		if(tmp == NULL) {
			int tmp = errno;
			free(iteml_begin);
			free(itemq_begin);
			errno = tmp;
			_return_err;
		}

		itemq_begin = tmp;
		itemq_end = itemq_begin + new_cap;
	}

	errno = 0;
	return (struct uint_vector__uint_pair_vector__pair){
		.first_begin = iteml_begin,
		.first_end = iteml_end,

		.second_begin = itemq_begin,
		.second_end = itemq_end
	};

	#undef _return_err
}
//mfederczuk zone end

static PyObject* getrenderbuck(PyObject* self,PyObject* args){
	PyObject* pytems;
	if(!PyArg_ParseTuple(args, "O", &pytems))
		return NULL;
	uint_fast64_t len=PyList_Size(pytems);
	uint_fast64_t items[len];
	for(uint_fast64_t i=0;i<len;i++){
		items[i]=PyLong_AsLong(PyList_GetItem(pytems,i));;
	}
	struct uint_vector__uint_pair_vector__pair result = get_render_buck(items, items + len);
	free(items);
	
	if(result.first_begin == NULL) {
		perror("get_render_buck");
		return NULL;
	}
	
	uint_fast64_t* iteml=result.first_begin;
	uint_fast64_t lsize=result.first_end-iteml;
	struct uint_pair* itemq=result.second_begin;
	uint_fast64_t qsize=result.second_end-itemq;
	
	PyObject* pyteml=PyTuple_New(lsize);
	PyObject* pytemq=PyTuple_New(qsize);
	uint_fast64_t i;
	for(i=0;i<lsize;i++){
		PyTuple_SetItem(pyteml,i,PyLong_FromLongLong(iteml[i]));
	}
	
	PyObject* tup;
	for(i=0;i<qsize;i++){
		tup=PyTuple_New(2);
		PyTuple_SetItem(tup,0,PyLong_FromLongLong(itemq[i].first));
		PyTuple_SetItem(tup,1,PyLong_FromLongLong(itemq[i].second));
		PyTuple_SetItem(pytemq,i,tup);
	}
	
	tup=PyTuple_New(2);
	PyTuple_SetItem(tup,0,pyteml);
	PyTuple_SetItem(tup,1,pytemq);
	free(iteml);
	free(itemq);
	return tup;
}

static PyMethodDef HelperMethods[] = {
    {"getrenderbuck",  getrenderbuck, METH_VARARGS, "Calculate stuff"},
    {NULL, NULL, 0, NULL}// Sentinel
};

static struct PyModuleDef helpermodule = {
	PyModuleDef_HEAD_INIT,
	"helper",	// name of module
	NULL,		// module documentation, may be NULL
	-1,			// size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    HelperMethods
};

PyMODINIT_FUNC PyInit_helper(void){
    return PyModule_Create(&helpermodule);
}

int main(int argc,char* argv[]){
	wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    /* Add a built-in module, before Py_Initialize */
    if (PyImport_AppendInittab("helper", PyInit_helper) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);
    /* Initialize the Python interpreter.  Required.
       If this step fails, it will be a fatal error. */
    Py_Initialize();
    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    if (!PyImport_ImportModule("helper")) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'helper'\n");
    }
    PyMem_RawFree(program);
    return 0;
}