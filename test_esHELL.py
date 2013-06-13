from es_HELL import *
import es_HELL as eh
from mock import Mock

# iter = 0

# def fake():
# 	global iter
# 	if iter==0:
# 		iter += 1
# 		return 'pop LS'
# 	elif iter==1:
# 		iter += 1
# 		return 'pop LS'
# 	else:
# 		return 'ciao'

class TestHell:
	def test_value_formatter(self):
		assert value_formatter("si") == True
		assert value_formatter("no") == False
		assert value_formatter("fkjhs") == 'fkjhs'
		assert value_formatter("  i ") == 'i'
		
	def test_value_formatter_inv(self):
		assert value_formatter_inv(['Pinco','Pallo','25',True]) == ['Pinco','Pallo','25','True']

	def test_value_formatter_inv_undo(self):
		assert value_formatter_inv_undo(['Pinco','Pallo','25',True]) == 'Pinco;Pallo;25;si'

	def test_show_contact_head(self, monkeypatch):
		assert show_contact_head(['Pinco','Pallo','25',True]) == 'Pinco Pallo'
		
		monkeypatch.setattr(eh, "value_formatter", Mock(return_value = "o"))
		contact = ['Pinco','Pallo','25',True]
		show_contact_head(contact)
		assert eh.value_formatter.call_count == len(contact[:2])

	def test_show_contact_list(self, monkeypatch):
		assert show_contact_list('Pinco;Pallo;25;si') == ['Pinco','Pallo','25',True]

		monkeypatch.setattr(eh, "value_formatter", Mock(return_value = "o"))
		contact = 'Pinco;Pallo;25;si'
		show_contact_list(contact)
		assert eh.value_formatter.call_count == 4 

	def test_show_contact_info(self, monkeypatch):
		monkeypatch.setattr(eh, "show_contact_list", Mock(return_value = ['Pinco','Pallo','25',True]))
		contact = 'Pinco;Pallo;25;si'
		show_contact_info(contact)
		assert eh.show_contact_list.called

	def test_initial_of_word(self):
		assert initial_of_word(['Pinco','Pallo','25',True]) == 'PP'

	def test_parse_cmd(self):
		c1 = 'add'
		c2 = 'Pinco;Pallo;25;si'
		assert parse_cmd(c1+' '+c2) == (c1,c2)

	def test_show_diz(self,monkeypatch):
		diz = {'a':'1','b':'2'}
		monkeypatch.setattr(eh, "value_formatter_inv", Mock(return_value = diz.values()))
		show_diz(diz)
		assert eh.value_formatter_inv.call_count == len(diz)

	def test_sort(self,monkeypatch):
		diz = {'a':['io','boh','20','True'],'b':['tu','mah','12','False']}
		assert sort('3',diz) == 'tm - tu mah 12 False\nib - io boh 20 True\n'

		monkeypatch.setattr(eh, "initial_of_word", Mock(return_value = 'aa'))
		monkeypatch.setattr(eh, "value_formatter_inv", Mock(return_value = 'Pinco;Pallo;25;True'))
		sort('3',diz)
		assert eh.initial_of_word.call_count == len(diz)
		assert eh.value_formatter_inv.call_count == len(diz)


	def test_add(self):
		diz = {'aa':['io','boh','20','True'],'bb':['tu','mah','12','False']}
		len1 = len(diz)
		add('Pinco;Pallo;15;si',diz)
		assert len(diz) == len1 + 1
		ciao =  ['Pinco','Pallo','15','True'] in diz.values()
		assert ciao == True

	def test_pop(self,monkeypatch):
		diz = {'aa':['io','boh','20','True'],'bb':['tu','mah','12','False'], 'PP':['Pinco','Pallo','15','True']}
		len1 = len(diz)
		pop('PP',diz)
		assert len(diz) == len1 -1
		var = 'PP' in diz.keys()
		assert var == False

		monkeypatch.setattr(eh, "value_formatter_inv_undo", Mock(return_value = 'Pinco;Pallo;25;si'))
		pop('bb',diz)
		assert eh.value_formatter_inv_undo.call_count == 1
		pop('bb',diz)
		pop('aa',diz)
		assert eh.value_formatter_inv_undo.call_count == 2

	def test_undo(self,monkeypatch,capsys):
		diz = {'ib':['io','boh','20','True'],'tm':['tu','mah','12','False'], 'PP':['Pinco','Pallo','15','True']}
		diz2 = diz.copy()

		pop('ib',diz)
		monkeypatch.setattr(eh, "last_command", "pop")
		undo(diz)
		assert diz == diz2

		add('bingo;bongo;52;no',diz)
		monkeypatch.setattr(eh, "last_command", "add")
		undo(diz)
		assert diz == diz2
		
		monkeypatch.setattr(eh, "last_command", "undo")
		undo(diz)
		assert diz == diz2

		# verifico che se chiamo la add, l'undo chiami la pop
		monkeypatch.setattr(eh, "pop", Mock())
		add('bingo;bongo;52;no',diz)
		monkeypatch.setattr(eh, "last_command", "add")
		monkeypatch.setattr(eh, "last_out", "bb")
		undo(diz)
		assert eh.pop.call_count == 1

		# verifico che se chiamo la pop, l'undo chiami la add
		monkeypatch.setattr(eh, "add", Mock())
		pop('ib',diz)
		monkeypatch.setattr(eh, "last_command", "pop")
		monkeypatch.setattr(eh, "last_out", "io;boh;20;si")
		undo(diz)
		assert eh.add.call_count == 1

		diz = diz2.copy()

		s = sort('3',diz)
		monkeypatch.setattr(eh, "last_out", s)
		monkeypatch.setattr(eh, "last_command", "sort")
		sort('2',diz)
		capsys.readouterr() #cattura quello che viene stampato fino a qua e azzera stdout e sdterr
		undo(diz)
		out, err = capsys.readouterr() #in questo modo mi da' quello che mi serve
		assert out == s + '\n'
		assert s == eh.last_out
		

	# def test_main(self, monkeypatch):
	# 	#monkeypatch.setattr(eh, "last_out", '')
	# 	#monkeypatch.setattr(eh, "fine", eh.last_out)
	# 	#monkeypatch.setattr(eh, "last_command", 'a')
	# 	monkeypatch.setattr(eh, "fine", '')
	# 	c = Mock(side_effect = fake)
	# 	monkeypatch.setattr(eh, "ask_user_input", c)
	# 	monkeypatch.setattr(eh, "pop", Mock(return_value = 'xxx'))
	# 	main()
	# 	assert eh.ask_user_input.call_count == 2
	# 	assert eh.last_command == ''
	# 	#assert eh.pop.call_count == 1


	def test_caller(self,monkeypatch):
	#	diz = {'ib':['io','boh','20','True'],'tm':['tu','mah','12','False'], 'PP':['Pinco','Pallo','15','True']}
		diz = Mock()
		monkeypatch.setattr(eh, "pop", Mock(return_value = ''))
		monkeypatch.setattr(eh, "add", Mock(return_value = ''))
		monkeypatch.setattr(eh, "sort", Mock(return_value = ''))
		monkeypatch.setattr(eh, "save_to_file", Mock(return_value = ''))
		monkeypatch.setattr(eh, "undo", Mock(return_value = ''))
		caller('pop ib', diz)
		assert eh.pop.called
		caller('add Mario;Rossi;55;no', diz)
		assert eh.add.called
		caller('sort 3', diz)
		assert eh.sort.called
		caller('save nome.txt', diz)
		assert eh.save_to_file.called
		caller('undo', diz)
		assert eh.undo.called
		
if __name__ == "__main__":
	import pytest
	pytest.main('test_esHELL.py')