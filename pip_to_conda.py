pip_to_conda = lambda a: '"'+'" "'.join(line.replace("==", " ") for line in a.split('\n'))+'"'
