run # Testing PROFOUND 2001

## 1. Start the System
Open your terminal in `c:\Users\ASUS\Desktop\Reverse learning` and run:

```bash
python -m profound2001.main
```

## 2. Try the Basics
Once inside the `> ` prompt:

| Command | Description |
| :--- | :--- |
| `run hello_world` | Runs the classic hello world pattern. |
| `run add` | Runs the canonical Add pattern (0 + 0 = 0). |
| `run sub` | Runs the canonical Sub pattern (0 - 0 = 0). |

## 4. Test "Growth" (Assimilation)
I have created `external_lib.py` in your folder. Swallow it whole:

```bash
> assimilate profound2001/external_lib.py
```
*Output: Ingested multiply.py, Ingested divide.py, Registered pattern: multiply...*

## 5. Test Data Inputs (New)
Patterns like `multiply` require inputs. Use `set`:

```bash
> set a 10
> set b 5
> run multiply
```
*Output: multiply: 50*

```bash
> run divide
```
*Output: divide: 2.0*

## 6. Test "Artifacts" (Bundling)
Turn your logic into a standalone executable:

```bash
> bundle hello_world my_app_v1.py
```
*Output: Bundled: my_app_v1.py*

Exit and test your artifact:
```bash
> exit
python my_app_v1.py
```

## 7. Test Constitution Enforcement
Try to assimilate a bloated file (I've created `profound2001/huge.py` for you):

```bash
> assimilate profound2001/huge.py
```
*Output: Assimilation failed: Method 'execute' exceeds 22 lines (29).*

**The system correctly rejects bloated logic.**
