import argparse
from src.train import train
from src.evaluate import evaluate
from src.predict import predict


def main():
    parser = argparse.ArgumentParser(description='FNDEC - Fake News Detection Classifier')
    subparsers = parser.add_subparsers(dest='command')

    # Train
    train_parser = subparsers.add_parser('train', help='Train the model')
    train_parser.add_argument('--data', required=True, help='Path to CSV dataset')
    train_parser.add_argument('--model', default='logistic_regression',
                              choices=['logistic_regression', 'passive_aggressive', 'naive_bayes'],
                              help='Classifier to use')
    train_parser.add_argument('--test-size', type=float, default=0.2, help='Test split ratio')
    train_parser.add_argument('--no-plot', action='store_true', help='Skip confusion matrix plot')

    # Predict
    predict_parser = subparsers.add_parser('predict', help='Predict on a single article')
    predict_parser.add_argument('--text', required=True, help='News article text to classify')
    predict_parser.add_argument('--model', default='logistic_regression',
                                choices=['logistic_regression', 'passive_aggressive', 'naive_bayes'])

    args = parser.parse_args()

    if args.command == 'train':
        pipeline, X_test, y_test = train(args.data, args.model, args.test_size)
        evaluate(pipeline, X_test, y_test, show_plot=not args.no_plot)

    elif args.command == 'predict':
        result = predict(args.text, args.model)
        print(f"\nResult: {result['label']}")
        if 'confidence' in result:
            print(f"Confidence: {result['confidence'] * 100:.1f}%")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
