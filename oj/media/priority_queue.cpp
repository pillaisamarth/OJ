#include<bits/stdc++.h>
using namespace std;
struct Item{
	int data, priority;
	int compareTo(Item other){
		int diff = priority - other.priority;
		if(diff > 0)
			return 1;
		else if(diff < 0)
			return -1;
		return 0;
	}
};	
class Heap{
	vector<Item> contents;
	int numItems;
	public:
	Heap(int maxSize){
		contents.resize(maxSize);
		numItems = 0;
	}
	Heap(){}
	Heap(vector<Item> &v){
		numItems = v.size();
		contents.resize(numItems);
		for(int i = 0; i < numItems; i++){
			contents[i] = v[i];
		}
		makeHeap();
		for(int i = 0; i < numItems; i++){
			v[i] = contents[i];
		}
	}
	void siftDown(int i){
		Item itemToSift = contents[i];
		int parent = i;
		int child = 2 * i + 1;
		while(child < numItems){
			if(child + 1 < numItems && contents[child].compareTo(contents[child + 1]) < 0){
				child += 1;
			}
			if(itemToSift.compareTo(contents[child]) >= 0)
				break;
			contents[parent] = contents[child];
			parent = child;
			child = 2 * parent + 1;
		}
		contents[parent] = itemToSift;
	}
	Item remove(){
		Item largest = contents[0];
		contents[0] = contents[numItems - 1];
		numItems -= 1;
		siftDown(0);
		return largest;
	}
	void insert(Item temp){
		if(numItems == contents.size()){
			contents.push_back(temp);
		}
		contents[numItems] = temp;
		siftUp(numItems);
		numItems += 1;
	}
	void siftUp(int i){
		Item itemToSift = contents[i];
		int parent = (i - 1) / 2;
		int child = i;
		while(parent >= 0){
			if(itemToSift.compareTo(contents[parent]) < 0)
				break;
			contents[child] = contents[parent];
			child = parent;
			if(parent == 0) break;
			parent = (child - 1) / 2;
		}
		contents[child] = itemToSift;
	}
	void makeHeap(){
		int last = numItems - 1;
		int parentOfLast = (last - 1) / 2;
		for(int i = parentOfLast; i >= 0; i--){
			siftDown(i);
		}
	}
	void print(){
		for(int i = 0; i < numItems; i++){
			cout << contents[i].data << " ";
		}
	}
};
class HeapSort{
	public:
	void Sort(vector<Item> &v){
		Heap heap(v);
		int endSorted = v.size() - 1;
		while(endSorted >= 0){
			Item largest = heap.remove();
			v[endSorted] = largest;
			endSorted -= 1;
		}
	}
};
int main(){
	int n;
	cout << "Enter the number of elements\n";
	cin >> n;
	cout << "\nNow enter the elements\n";
	vector<Item> v;
	for(int i = 0; i < n; i++){
		int a;
		cin >> a;
		v.push_back({a, a});
	}
	HeapSort hs;                // Replace heapsort with heap to check if the heap class is working or not
	hs.Sort(v);
	for(int i = 0; i < n; i++){
		cout << v[i].data << " ";
	}
}
	