#!/usr/bin/env python3
"""
Model Training Example for Cloudera AI
Demonstrates a complete ML workflow including:
- Data loading and preprocessing
- Model training
- Evaluation and metrics
- Model saving
"""

import os
import sys
import argparse
import logging
import json
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging with the specified level"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Model Training Job")
    
    parser.add_argument(
        "--n_samples",
        type=int,
        default=1000,
        help="Number of samples to generate"
    )
    
    parser.add_argument(
        "--n_features",
        type=int,
        default=20,
        help="Number of features"
    )
    
    parser.add_argument(
        "--model_name",
        type=str,
        default="random_forest_model",
        help="Name for the saved model"
    )
    
    parser.add_argument(
        "--output_dir",
        type=str,
        default="results",
        help="Directory to save model and results"
    )
    
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    
    return parser.parse_args()


def generate_data(n_samples: int, n_features: int) -> tuple:
    """Generate synthetic classification data"""
    logger = logging.getLogger(__name__)
    logger.info(f"Generating {n_samples} samples with {n_features} features")
    
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_features//2,
        n_redundant=0,
        n_classes=2,
        random_state=42
    )
    
    return X, y


def train_model(X_train, y_train, n_estimators: int = 100) -> RandomForestClassifier:
    """Train a Random Forest classifier"""
    logger = logging.getLogger(__name__)
    logger.info(f"Training Random Forest with {n_estimators} estimators")
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    logger.info("Model training complete")
    
    return model


def evaluate_model(model, X_test, y_test) -> dict:
    """Evaluate the trained model"""
    logger = logging.getLogger(__name__)
    logger.info("Evaluating model performance")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    results = {
        "accuracy": accuracy,
        "classification_report": report,
        "test_size": len(y_test),
        "training_date": datetime.now().isoformat()
    }
    
    logger.info(f"Model accuracy: {accuracy:.4f}")
    
    return results


def save_results(model, results: dict, output_dir: str, model_name: str) -> None:
    """Save model and results"""
    logger = logging.getLogger(__name__)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, f"{model_name}.pkl")
    joblib.dump(model, model_path)
    logger.info(f"Model saved to: {model_path}")
    
    # Save results
    results_path = os.path.join(output_dir, f"{model_name}_results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)
    logger.info(f"Results saved to: {results_path}")
    
    # Save feature importances
    if hasattr(model, 'feature_importances_'):
        importances = pd.DataFrame({
            'feature': [f'feature_{i}' for i in range(len(model.feature_importances_))],
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importances_path = os.path.join(output_dir, f"{model_name}_feature_importances.csv")
        importances.to_csv(importances_path, index=False)
        logger.info(f"Feature importances saved to: {importances_path}")


def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting model training job")
        
        # Generate data
        X, y = generate_data(args.n_samples, args.n_features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(f"Data split - Train: {len(X_train)}, Test: {len(X_test)}")
        
        # Train model
        model = train_model(X_train, y_train)
        
        # Evaluate model
        results = evaluate_model(model, X_test, y_test)
        
        # Save everything
        save_results(model, results, args.output_dir, args.model_name)
        
        logger.info("Model training job completed successfully")
        
    except Exception as e:
        logger.error(f"Error in model training job: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()