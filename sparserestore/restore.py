from . import backup, perform_restore

def restore_file(fp: str, restore_path: str, restore_name: str):
    contents = open(fp, "rb").read()

    back = backup.Backup(files=[
        backup.Directory("", f"SysContainerDomain-../../../../../../../../var/backup{restore_path}", owner=33, group=33),
        backup.ConcreteFile("", f"SysContainerDomain-../../../../../../../../var/backup{restore_path}{restore_name}", owner=33, group=33, contents=contents),
        backup.ConcreteFile("", "SysContainerDomain-../../../../../../../.." + "/crash_on_purpose", contents=b"")
    ])

    perform_restore(backup=back)
