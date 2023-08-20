
# Обработчик кнопки "Отмена" при заполнении резюме
@router.message(lambda message: message.text == text.cancel)
async def Cancel_button(message: Message, state: FSMContext):
    curent_state = await state.get_state()
    if curent_state == Resume.name:
        await state.set_state(Resume.start)
        await message.answer("Вы вернулись в начало", reply_markup=kb.Main_keyboard)
    elif curent_state == Resume.surname:
        await state.set_state(Resume.name)
        await message.answer("Вы вернулись к заполнению имени", reply_markup=kb.Cancel_panel)
    elif curent_state == Resume.patronymic:
        await state.set_state(Resume.surname)
        await message.answer("Вы вернулись к заполенению фамиллии", reply_markup=kb.Cancel_panel)
    else:
        await message.answer("Нет такого состояния")
