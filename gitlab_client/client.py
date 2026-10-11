
import io
import gitlab

class GitLabClient:

    git = gitlab.Gitlab(url='https://gitlab.com/', private_token='glpat-frrUF4RUHIeG2CT9jKcpK2M6MQpvOjEKdTpwbzdpdQ8.01.170egvky3')
    project = git.projects.get('null-group5064341/cloud_point_test')
    

    def get_unit_files(self) -> list[io.StringIO]:

        yaml_content = []
        repo_files = self.project.repository_tree(ref='main', recursive=True, all=True)

        for item in repo_files:
            if item['type'] == 'blob' and (item['path'].endswith('.yaml') or item['path'].endswith('.yml')):
                file_path = item['path']
                try:
                    file_info = self.project.files.get(file_path=file_path, ref='main')
                    file_content = file_info.decode().decode('utf-8')

                    buffer = io.StringIO(file_content)
                    yaml_content.append(buffer)
                except Exception as e:
                    print(f"Error to get yaml file with path \'{file_path}\' : {e}")

        return yaml_content
