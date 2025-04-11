CREATE TABLE IF NOT EXISTS projects (
	projectId integer primary key NOT NULL UNIQUE,
	projectName TEXT NOT NULL,
	projectDescription TEXT NOT NULL,
	imagePath TEXT NULL,
	activeProject Integer DEFAULT 1
);

CREATE TABLE IF NOT EXISTS projectDetails (
	projectId integer primary key NOT NULL UNIQUE,
	hasPreview Integer NULL,
	hasGitRepo Integer NULL,
	allImagePath TEXT NULL,
	overview TEXT NULL,
	problemStatement TEXT NULL,
	solutionApproach TEXT NULL,
	createdDt DATETIME NULL,
	lastUpdateDt DATETIME NULL,
FOREIGN KEY(projectId) REFERENCES projects(projectId)
);

CREATE TABLE IF NOT EXISTS projectTechStack (
	projectId integer NOT NULL,
	techStackName TEXT NULL,
FOREIGN KEY(projectId) REFERENCES projects(projectId)
);

CREATE TABLE IF NOT EXISTS inquiryMessages (
	messageId integer primary key NOT NULL UNIQUE,
	requestorName TEXT NOT NULL,
	requestorEmailAddress TEXT NOT NULL,
	subjectLine TEXT NOT NULL,
	messageDescription TEXT NOT NULL,
	sentDatetime DATETIME NULL,
	isProcessed Integer NULL
);