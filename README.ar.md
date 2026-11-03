# خط عربي جميل لتطبيق Claude

[فارسی](README.md) · [English](README.md#english)

تطبيق Claude لسطح المكتب على ماك يعرض النص العربي بالخط الافتراضي للنظام، وهو غير مريح للقراءة. هذه الإضافة تغيّر خط النص العربي (والفارسي والأردو) إلى خط تختاره. يأتي معها خط **Vazirmatn** الذي يدعم العربية، ويمكنك إضافة أي خط عربي تملكه.

النص الإنجليزي والأكواد لا تتغيّر؛ تتغيّر الحروف العربية فقط.

## التثبيت

### الأسهل: اطلب ذلك من Claude

أعطِ Claude رابط هذه الصفحة وقل له:

> ثبّت لي هذا: https://github.com/MoAliTheGoat/claude-persian-font

### يدويًا

في تطبيق Claude: اضغط **+** بجانب صندوق الرسائل ← **Plugins** ← **Add marketplace** ← اكتب `MoAliTheGoat/claude-persian-font` ← ثم أضف **persian-font**.

أو في Claude Code:

```
/plugin marketplace add MoAliTheGoat/claude-persian-font
/plugin install persian-font@claude-persian-font
```

ثم أغلق Claude مرة واحدة (Cmd+Q) وافتحه من جديد.

## الاستخدام

فوق صندوق الرسائل زر صغير **«Aa»**؛ اضغطه لتظهر الخطوط. عند اختيار خط يُغلق Claude ويُفتح من جديد تلقائيًا خلال ثوانٍ، لأن Claude يقرأ الخطوط عند بدء التشغيل فقط. زر «پنهان کن» يخفي الشريط، والأمر `/persian-font` يعيده.

## إضافة خطك العربي

ضع ملفات الخط (`.ttf` أو `.otf`، العادي والعريض على الأقل) في مجلد باسم الخط:

```
~/.claude-persian-font/fonts/<اسم الخط>/
```

مثلًا `~/.claude-persian-font/fonts/Cairo/`. بعد إعادة فتح Claude يظهر الخط في القائمة.

## ويندوز

على ويندوز يتغيّر **نص ردود Claude فقط**؛ القوائم ورسائلك تبقى بخط ويندوز (Segoe UI) لأنه يحتوي على حروف عربية ويأتي أولًا. في PowerShell:

```powershell
irm https://raw.githubusercontent.com/MoAliTheGoat/claude-persian-font/main/windows/install.ps1 | iex
```

ثم في Claude: Settings ← Appearance ← **Response font** ← اختر Serif، وأغلق Claude بالكامل وافتحه. للخط في كل الواجهة على ويندوز استخدم Claude في المتصفح مع إضافة [RTL for Claude](https://github.com/mahdigh99/rtl-for-claude).

## قيود معروفة

- كل تغيير للخط يحتاج إعادة تشغيل Claude (يتم تلقائيًا من الزر).
- إذا تغيّر الخط ولم يُعَد تشغيل Claude، قد تظهر الحروف مربعات حتى إعادة التشغيل.
- لا يمكن إضافة الخطوط إلى قائمة Settings ← Interface font داخل Claude.
