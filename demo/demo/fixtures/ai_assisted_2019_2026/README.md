# AI-assisted synthetic sample data: 2019–2026

This dataset is a new, synthetic addition created with Copilot assistance on
2026-10-01. It is intentionally separate from the original fixtures in
`demo/demo/fixtures/`; those original files have not been edited for this
dataset.

`dataset.json` is the input specification. The explicitly invoked Django
management command `python manage.py load_ai_assisted_dataset` reads it and
creates an `ai-managed` login, a separate client, and associated records. This
account owns only this synthetic farm; the Berkeley and Foster accounts and
their data remain separate. The command can also transfer a previously loaded
synthetic farm from the Foster account to the new account. It does not delete
or replace existing records and is safe to rerun.

The new account is created with an unusable password. Set a local password
explicitly before logging in:

```sh
python manage.py changepassword ai-managed
```

The fixed scenario has eight tagged cows purchased in 2019; monthly milking,
event, and exercise records; quarterly health inspections; and seasonal seed
records through 2026. Milk volumes vary by cow, season, and year. The health
records include a small, repeatable mix of illness and injury cases as well as
healthy and pregnant checkups. These are explicitly synthetic scenarios, not
real herd records or medical guidance. Rerunning the loader updates this
dataset's generated milk and health details and recalculates its reports.

To load it into a local database after the original fixtures are installed:

```sh
cd demo
python manage.py load_ai_assisted_dataset
```

Loading is not part of migrations or Reload Cache. Do not export the generated
records over the original fixture files.
