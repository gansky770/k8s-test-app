pipelineJob("k8stest-pipeline") {
	description()
	keepDependencies(false)
	definition {
		cpsScm {
			scm {
				git {
					remote {
						github("gansky770/k8s-test-app", "ssh")
						credentials("git")
					}
					branch("*/development")
				}
			}
			scriptPath("Jenkinsfile")
		}
	}
	disabled(false)
}