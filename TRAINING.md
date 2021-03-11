## Training

It might be desirable to train own pairs to capture the specifics of the dataset at hand. Figuring out which pairs should be merged can be highly subjective.

- `"อ" + "ง" | (meaningless token) + (meaningless token) = (meaningless token)"`
  - Merged because all 3 are meaningless tokens and the result is expected to become a part of a larger token.
- `"ส่ง" + "ฟรี" | free + delivery -> freedelivery`
  - Separate since merging does not change the meaning of individual words.
- `"กาญจนา" + "ภิเษก" | kanjana + pisek = Kanajanapisek`
  - Given names should be merged.
- `"แบต" + "เตอรี่" | batt + tery = battery`
  - Merged because it is an anglicism.
- `"จักร" + "ยาน" | sewing machine + spacecraft = bicycle`  
  - Merged because the new token produces a token unrelated to the joined parts.
- `"ตำ" + "นาน" | pound + long = legend`
  - Same as above example.
- `"ต่าง" + "หู" | different + ear = earrings`
  - Merged because of significant alteration in the meaning.
- `"กระ" + "เป๋า" | freckles + pouch = handbag`
  - Merged because of significant alteration in meaning, additionally, the result produces a common word for everyday use.
- `"เสื้อ" + "เชิ้ต" | shirt + _modifier_word_ = button up shirt`
  - Separate because "shirt" should be available for full text matching. The modifier will be found through bi-gram matching.

```bash
git clone thai_tokenizer
cd thai_tokenizer
python3 -m thai_tokenizer --help
```