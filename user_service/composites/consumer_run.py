from user_service.composites.app_api import ConsumerMessageBus

if __name__ == '__main__':
    ConsumerMessageBus.declare_scheme()
    ConsumerMessageBus.consumer.run()