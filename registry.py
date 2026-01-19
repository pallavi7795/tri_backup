from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import CompilationStep, RegisterModel
from sagemaker.workflow.model_step import ModelStep
from sagemaker.workflow.pipeline_context import PipelineSession

# Set up pipeline session
pipeline_session = PipelineSession()

# ... (previous compilation step code) ...

# Create register model step
register_model_step = RegisterModel(
    name="RegisterCompiledModel",
    model=pytorch_model,  # Your model object
    content_types=["application/x-image", "application/json"],
    response_types=["application/json"],
    inference_instances=["ml.c5.xlarge", "ml.p3.2xlarge"],
    transform_instances=["ml.c5.xlarge", "ml.p3.2xlarge"],
    model_package_group_name=model_package_group_name,
    approval_status="PendingManualApproval",
    model_metrics={
        "mAP": {
            "value": 0.85,
            "standard_deviation": 0.02
        }
    },
    depends_on=[compilation_step]  # Depends on the compilation step
)

# Create the pipeline with both steps
pipeline = Pipeline(
    name="CompileAndRegisterPipeline",
    steps=[compilation_step, register_model_step],
    sagemaker_session=pipeline_session
)

# Submit the pipeline definition
pipeline.upsert(role_arn=role)

# Start the pipeline execution
execution = pipeline.start()